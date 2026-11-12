/* Letter-size student handout pagination, shared by on-screen preview and printing.
 * Keep this separate from the lesson/question generators so a page-layout change
 * cannot alter mathematical content or the Plan and Teacher key views. */
(function (G) {
  'use strict';
  var doc = G.document;
  var P = G.MKPLAN = G.MKPLAN || {};

  /* A section can span sheets. Split at sensible boundaries: problem rows,
     note cards, worked-example pairs, and table rows. */
  function makePieces(html) {
    var scratch = doc.createElement('div');
    scratch.innerHTML = html;
    var source = scratch.querySelector('.pl-sheet');
    if (!source) throw new Error('Student handout is missing');
    var pieces = [], tableId = 0, sectionId = 0;

    function add(node, section, wrappers) {
      wrappers = wrappers || [];
      if (node.classList && node.classList.contains('nt')) {
        Array.prototype.forEach.call(node.children, function (child) {
          add(child, section, wrappers.concat([node]));
        });
        return;
      }
      if (node.classList && node.classList.contains('nt-wes') && node.children.length > 2) {
        var children = Array.prototype.slice.call(node.children);
        for (var i = 0; i < children.length; i += 2) {
          var pair = node.cloneNode(false);
          pair.appendChild(children[i].cloneNode(true));
          if (children[i + 1]) pair.appendChild(children[i + 1].cloneNode(true));
          pieces.push({node:pair, section:section, wrappers:wrappers});
        }
        return;
      }
      if (node.tagName === 'TABLE' && node.tBodies.length) {
        var rows = Array.prototype.slice.call(node.tBodies[0].rows);
        if (rows.length) {
          var id = ++tableId;
          rows.forEach(function (row) {
            pieces.push({node:row, section:section, wrappers:wrappers, tableId:id, tableSource:node});
          });
          return;
        }
      }
      pieces.push({node:node, section:section, wrappers:wrappers});
    }

    Array.prototype.forEach.call(source.children, function (node) {
      if (!node.classList || (!node.classList.contains('pl-sbox') && !node.classList.contains('pl-exit'))) {
        add(node, null, []);
        return;
      }
      var section = {
        id:++sectionId, className:node.className,
        heading:node.querySelector(':scope > .pl-shd'),
        cut:node.querySelector(':scope > .pl-cut')
      };
      var before = pieces.length;
      Array.prototype.forEach.call(node.children, function (child) {
        if (child === section.heading || child === section.cut) return;
        add(child, section, []);
      });
      /* An empty user-selected section should still appear on the handout. */
      if (before === pieces.length) pieces.push({node:doc.createElement('div'), section:section, wrappers:[]});
    });
    return pieces;
  }

  function wrap(node, wrappers) {
    for (var i = wrappers.length - 1; i >= 0; i--) {
      var parent = wrappers[i].cloneNode(false);
      parent.appendChild(node);
      node = parent;
    }
    return node;
  }

  function createPage(stage) {
    var page = doc.createElement('section');
    page.className = 'pl-sheet pl-page';
    var content = doc.createElement('div');
    content.className = 'pl-page-content';
    page.appendChild(content);
    stage.appendChild(page);
    return {page:page, content:content, section:null, shell:null, table:null, count:0};
  }

  function overflowing(page) {
    /* scrollHeight respects the real screen font, KaTeX and inline SVG sizes. */
    return page.content.scrollHeight > page.content.clientHeight + 1;
  }

  /* Returns detached, fully laid-out page elements. These exact nodes can be
     displayed for preview or sent to #printRoot without reflowing the sections. */
  P.paginateStudent = function (html) {
    var pieces = makePieces(html);
    var stage = doc.createElement('div');
    stage.className = 'pl-measure-stage';
    doc.body.appendChild(stage);
    var pages = [], current;
    function nextPage() { current = createPage(stage); pages.push(current); }
    nextPage();

    function place(piece) {
      var oldSection = current.section, oldShell = current.shell, oldTable = current.table;
      var createdShell = false, placed;
      var parent = current.content;
      if (piece.section) {
        if (!current.shell || current.section !== piece.section) {
          var shell = doc.createElement('div');
          shell.className = piece.section.className;
          /* The cut line belongs only to the original start of an exit ticket. */
          if (piece.section.cut && !pieces.slice(0, pieces.indexOf(piece)).some(function (p) { return p.section === piece.section; }))
            shell.appendChild(piece.section.cut.cloneNode(true));
          if (piece.section.heading) {
            var heading = piece.section.heading.cloneNode(true);
            if (pieces.indexOf(piece) > pieces.findIndex(function (p) { return p.section === piece.section; })) {
              var cont = doc.createElement('small');
              cont.textContent = ' (continued)';
              heading.appendChild(cont);
            }
            shell.appendChild(heading);
          }
          current.content.appendChild(shell);
          current.shell = shell;
          current.section = piece.section;
          current.table = null;
          createdShell = true;
        }
        parent = current.shell;
      } else {
        current.section = current.shell = current.table = null;
      }

      if (piece.tableId && current.table && current.table.id === piece.tableId && current.table.parent === parent) {
        placed = piece.node.cloneNode(true);
        current.table.body.appendChild(placed);
      } else if (piece.tableId) {
        var table = piece.tableSource.cloneNode(false);
        Array.prototype.forEach.call(piece.tableSource.children, function (child) {
          if (child.tagName === 'COLGROUP' || child.tagName === 'THEAD') table.appendChild(child.cloneNode(true));
        });
        var tbody = doc.createElement('tbody');
        tbody.appendChild(piece.node.cloneNode(true));
        table.appendChild(tbody);
        placed = wrap(table, piece.wrappers);
        parent.appendChild(placed);
        current.table = {id:piece.tableId, parent:parent, body:tbody};
      } else {
        placed = wrap(piece.node.cloneNode(true), piece.wrappers);
        parent.appendChild(placed);
        current.table = null;
      }

      if (overflowing(current) && current.count > 0) {
        placed.remove();
        if (createdShell) current.shell.remove();
        current.section = oldSection;
        current.shell = oldShell;
        current.table = oldTable;
        nextPage();
        place(piece);
        return;
      }
      /* An individually oversized illustration/card cannot be fragmented
         without risking broken diagrams; show a warning instead of clipping it. */
      if (overflowing(current)) current.page.classList.add('pl-page-oversize');
      current.count++;
    }

    try {
      pieces.forEach(place);
      pages.forEach(function (record, i) {
        var page = record.page;
        page.setAttribute('aria-label', 'Handout page ' + (i + 1) + ' of ' + pages.length);
        page.setAttribute('data-page', String(i + 1));
        var label = doc.createElement('div');
        label.className = 'pl-page-label';
        label.textContent = 'Page ' + (i + 1) + ' of ' + pages.length;
        page.appendChild(label);
      });
      return pages.map(function (x) { return x.page; });
    } finally {
      stage.remove();
    }
  };
})(window);

