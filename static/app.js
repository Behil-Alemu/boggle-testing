
class BoggleGame {
    /* make a new game at this DOM id */
  
    constructor(boardId, secs = 60) {
      this.secs = secs; // game length
      this.showTimer();
  
      this.score = 0;
      this.words = new Set();
      this.board = $("#" + boardId);
          // every 1000 msec, "tick"
      this.timer = setInterval(this.tick.bind(this), 1000);
  
      $("#input-word", this.board).on("submit", this.handleSubmit.bind(this));
    }
  
    /* show word in list of words */
  
    showWord(word) {
      $(".words", this.board).append($("<li>", { text: word }));
    }
  
    /* show score in html */
  
    showScore() {
      $(".score", this.board).text(this.score);
    }
  
    /* show a status message */
  
    showMessage(msg, cls) {
      $(".msg", this.board)
        .text(msg)
        .removeClass()
        .addClass(`msg ${cls}`);
    }
  
    /* handle submission of word: if unique and valid, score & show */
  
    async handleSubmit(evt) {
      evt.preventDefault();
      const $word = $(".word", this.board);
      // wait to get the input then check if it is valid  
  
      let word = $word.val();
      if (!word) return;
    // if there is no word, return nothing?

  
      if (this.words.has(word)) {
        this.showMessage(`Already found ${word}`, "err");
        return;
      }
      // if the word they input is already in the new object set() the return saying aready found
  
      // check server for validity
      const resp = await axios.get("/check-word", { params: { word: word }});
      if (resp.data.result === "not-word") {
        this.showMessage(`${word} is not a valid English word`, "err");
      } else if (resp.data.result === "not-on-board") {
        this.showMessage(`${word} is not a valid word on this board`, "err");
      } else {
        this.showWord(word);
        this.score += word.length;
        this.showScore();
        this.words.add(word);
        this.showMessage(`Added: ${word}`, "ok");
      }
    }
  
    /* Update timer in DOM */
  
    showTimer() {
      $(".timer", this.board).text(this.secs);
    }
  
    /* Tick: handle a second passing in game */
  
    async tick() {
      this.secs -= 1;
      this.showTimer();
  
      if (this.secs === 0) {
        clearInterval(this.timer);
        await this.scoreGame();
      }
    }
  
    /* end of game: score and update message. */
  
    async scoreGame() {
      $("#word", this.board).hide();
      const resp = await axios.post("/show-score", { score: this.score });
      if (resp.data.newRecord) {
        this.showMessage(`New record: ${this.score}`, "ok");
      } else {
        this.showMessage(`Final score: ${this.score}`, "ok");
      }
    }
  }
  // why hide on line 94?
  let play = new BoggleGame("container", 60)