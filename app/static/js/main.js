// Real articles drawn from the model's held-out test set (ground-truth labels included
// in the dataset). Kept at full length since short snippets don't carry enough TF-IDF signal.
const SAMPLE_ARTICLES = {
  "real-1": {
    title: "What Walker's Departure Means for GOP Field",
    text: "Wisconsin Gov. Scott Walker, a once rising star of the GOP presidential pack, has dropped out of the race. Now the field is scrambling to re-align.\n\nJust this summer, Walker led the Republican field in Iowa. But on Monday, he called it quits and suggested that someone could emerge from a smaller pool of candidates with a clear conservative alternative to the current frontrunner, Donald Trump.\n\n\"Today, I believe that I am being called to lead by helping to clear the race so that a positive conservative message can rise to the top of the field. With that in mind, I will suspend my campaign immediately,\" he said.\n\nBut will others drop out so that support can build around an alternative to Trump? None are expected to do so anytime soon. In fact, they're all vying for the Walker campaign assets.\n\nSome believe that Sen. Marco Rubio, R-Fla., will benefit the most from Walker's departure. They're both considered \"fresh faces\" with next generation appeal.\n\nLate Monday, Rubio was already welcoming Walker staff to his team, as was Sen. Ted Cruz, R-Texas.\n\nThe latest CNN poll shows political outsiders Trump, former Hewlett Packard CEO Carly Fiorina, and retired neurosurgeon Ben Carson leading the presidential pack, with Rubio and former Florida Gov. Jeb Bush in fourth and fifth place respectively.\n\nMeanwhile, on the Democratic side, Hillary Clinton is battling off an unexpectedly strong challenge from Sen. Bernie Sanders, I-Vt. She's also waiting to see if Vice President Joe Biden decides to enter the race.\n\nIn her latest campaign move, the former secretary of state is promising not only to protect Obamacare from GOP plans to repeal it, but to improve it.\n\n\"As the latest census numbers show, the number of uninsured continues to fall and Americans are now seeing, hearing, and feeling the full benefits of the Affordable Care Act,\" a Clinton campaign official said Saturday.\n\nIt's already a presidential campaign year that no one could have predicted, and voters have never had so many candidates to consider.\n\nBut whether any of them will follow Walker's advice to lead by falling back is unlikely for now."
  },
  "real-2": {
    title: "Cuba releases all 53 political prisoners to complete deal, U.S. official says",
    text: "Cuba has completed the release of 53 political prisoners that was part of last month's historic deal between the United States and Cuba, the U.S. said Monday.\n\nThe prisoners had been on a list of opposition figures whose release was sought as part of the U.S. agreement last month with the Cuban government. They had been cited by various human rights organizations as being imprisoned by the Cuban government for exercising internationally protected freedoms or for their promotion of political and social reforms in Cuba.\n\nThe U.S. has verified the release, according to an official traveling with U.S. Secretary of State John Kerry in Islamabad. The official spoke to the Associated Press on condition of anonymity because the official was not authorized to discuss the issue on the record.\n\nAmong those released were Haydee Gallardo S., a Lady in White, and her husband Angel Figueredo C. who were both arrested in May 2014 on charges of \"public disorder.\"\n\nThe independent rap artist Angel Yunier Remon Arzuaga, known as \"El Critico,\" was also released. El Critico was sentenced to eight years in prison without a trial in March 2013 for \"resistance\" against the communist regime.\n\nLast month, Cuba and the U.S. agreed to work to restore normal diplomatic relations as part of a deal in which Cuba freed an imprisoned U.S. aid worker, Alan Gross, along with an imprisoned spy working for the U.S. and the imprisoned dissidents. The U.S. released several Cuba intelligence agents. The deal came after 50 years of hostility between the two countries.\n\nThere had been much concern in the Cuban-American immigrant community and among aid workers, as well as from top U.S. conservatives like Sen. Marco Rubio, R-Fla, who is also a Cuban-American, about the lack of transparency and the secrecy surrounding the identities of the political prisoners.\n\nThe leader of the Miami-based Foundation for Human Rights in Cuba (FHRC), Francisco Hernandez, was highly vocal about the issue.\n\n\"We would like to know the names, because obviously these people are going to need help when they are released, and we want to make sure that they are released,\" Hernandez told Fox News Latino.\n\nBased on reporting by the Associated Press."
  },
  "fake-1": {
    title: "Breaking: We Have Proof That Hillary Clinton Rigged Half the Voting Machines In America!",
    text: "This is really, really bad guys. Hillary Clinton has found a guaranteed way to rig the vote, and America is completely clueless.\nVia AlternativeNews\n\nNow, we at Liberty Writers have come across indisputable proof that Dominion Voting Systems, the biggest voting machine owner in the US, has been rigged by Hillary Clinton!\nScroll Down For Video Below! So let's start off with a little fact from Wikipedia. Back in 2010, just in time to help Obama get elected again, Dominion Voting Machines bought out the right to own the machines in 22 different states.\n\nThe same company has also been caught red-handed donating enough money to the Clinton Foundation to make it to the top of their online donor list. Just take a look at the Clinton Foundation's website itself.\n\nWow. That is just such a strange coincidence, don't you think? Right around the same time Hillary Clinton was deciding to retire as Secretary of State and focus on her campaign, this company bought out half the voting machines in the country.\nAnd if that is not bad enough, one of the top owners of Dominion Voting is none other than the king of corruption himself, George Soros. So if you think this is as important of information as I do, then share this out immediately! Time is of the essence..."
  },
  "fake-2": {
    title: "Professor Shares Insights on Paranormal, Cannibalism and Vampires.",
    text: "Professor Shares Insights on Paranormal, Cannibalism and Vampires. # Edward777 0\nDurham University lecturer Richard Sugg deals with history and analysis of esoteric themes as well as corpse medicine in European history, vampirism in ancient and modern Europe, ghosts and poltergeists. He deals with how society sees these subjects, some explanations, some items that have no scientific explanations, and even the psychological basis for these topics. Some of these you may have heard about, most of his research is probably new to listeners. Tags"
  }
};

const form = document.getElementById("predict-form");
const titleInput = document.getElementById("title");
const textInput = document.getElementById("text");
const submitBtn = document.getElementById("submit-btn");
const sampleBtn = document.getElementById("sample-btn");
const wordCountEl = document.getElementById("word-count");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");
const badgeEl = document.getElementById("result-badge");
const confidenceFill = document.getElementById("confidence-fill");
const confidenceValue = document.getElementById("confidence-value");

function updateWordCount() {
  const words = textInput.value.trim().split(/\s+/).filter(Boolean).length;
  wordCountEl.textContent = words > 0 ? `${words} words` : "";
}
textInput.addEventListener("input", updateWordCount);

sampleBtn.addEventListener("click", () => {
  const keys = Object.keys(SAMPLE_ARTICLES);
  const randomKey = keys[Math.floor(Math.random() * keys.length)];
  const sample = SAMPLE_ARTICLES[randomKey];
  titleInput.value = sample.title;
  textInput.value = sample.text;
  updateWordCount();
  resultEl.classList.add("hidden");
  errorEl.classList.add("hidden");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorEl.classList.add("hidden");
  resultEl.classList.add("hidden");

  const title = titleInput.value.trim();
  const text = textInput.value.trim();
  if (!title && !text) {
    showError("Please enter a headline or article text to analyze.");
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = "Analyzing...";

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, text }),
    });
    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Something went wrong. Please try again.");
      return;
    }
    showResult(data);
  } catch (err) {
    showError("Could not reach the server. Is the Flask app running?");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Analyze Article";
  }
});

function showResult(data) {
  const isReal = data.label === "REAL";
  badgeEl.textContent = data.label;
  badgeEl.className = "result__badge " + (isReal ? "real" : "fake");
  confidenceValue.textContent = `${data.confidence}%`;
  confidenceFill.style.width = "0%";
  resultEl.classList.remove("hidden");
  requestAnimationFrame(() => {
    confidenceFill.style.width = `${data.confidence}%`;
  });
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.classList.remove("hidden");
}
