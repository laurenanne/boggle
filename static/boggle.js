let wordList = [];

async function checkWord(evt) {
  evt.preventDefault();
  let word = $(".word").val();
  let response = await axios.get("/check", { params: { word } });
  let result = response.data.answer;
  $(".word").val("");

  return showResponse(result, word);
}

$("#boggle-form").on("submit", checkWord);

let total = 0;

function showResponse(result, word) {
  let $div = $("#word-res");
  $div.html("");

  let reply;

  if (wordList.includes(word)) {
    reply = `${word} has already been played. Please try again`;
  } else if (result === "not-word") {
    reply = `${word} is not a word. Please try again`;
  } else if (result === "not-on-board") {
    reply = `${word} is not on the board. Please try again`;
  } else if (result === "ok") {
    reply = `Hooray! ${word} is on the board.`;
    wordList.push(word);
    total += word.length;
  }

  let $p = `<p>${reply}</p>`;
  let $score = `<p>score: ${total}</p>`;
  $div.append($p);
  $div.append($score);

  return;
}

let timer = 60;
myTimer = setInterval(updateClock, 1000);

function updateClock() {
  timer = timer - 1;
  $("#timer").html(timer);
  if (timer === 0) {
    console.log("Game Over");
    clearInterval(myTimer);
    wordList = [];
    alert("Game Over");

    $(":input[type=submit]").prop("disabled", true);

    return gameScore(total);
  }
}

async function gameScore(total) {
  let response = await axios.post("/post-score", { total: total });
  let highscore = response.data.highscore;
  let count = response.data.count;
  return showFinal(total, highscore, count);
}

function showFinal(total, highscore, count) {
  let $div = $("#word-res");
  $div.html("");

  let $score = `<p>score: ${total}</p>`;
  let $highscore = `<p>high score: ${highscore}</p>`;
  let $count = `<p>Number of times played: ${count}</p>`;

  $div.append($score);
  $div.append($highscore);
  $div.append($count);

  return;
}
