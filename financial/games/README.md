# Financial Algebra games

Five existing Classroom formats use the Financial Algebra authored question banks: Showdown, Connect 4, Tic-Tac-Toe, Picture Reveal, and Detective. Each unit links to this local launcher; no cross-site iframe or external runtime is required.

The files in `vendor/` are snapshots of `akneller1/classroom`'s `worksheet-generator/games/` engines plus `core/rng.js`. The only Financial Algebra engine change is Showdown's single Standard board preset. The authored-bank adapter in `deck.mjs` preserves scenarios, original choices, correct answers, and solution steps. Only game-eligible single-answer multiple-choice questions are used. Choices are shuffled without generating distractors. Decks avoid duplicate IDs and exhaust unseen questions before reusing them in subsequent rounds.

For Detective, select enough skills to supply ten distinct questions. An insufficient selection shows a message and a button to return to skill selection. The existing mystery's ten clues and accusation rules are preserved.

Run `node --test tests/financial-games.test.mjs`. Browser QA should start each game, answer a question, and check both feedback and board/evidence progression.
