let questions = []; // This will hold the questions loaded from the JSON file
let currentQuestionIndex = 0;
let userAnswers = [];

const loadQuestions = async () => {
  try {
    const response = await fetch('questions.json');
    questions = await response.json();
  } catch (error) {
    console.error('Failed to load questions:', error);
  }
};

const showQuestion = (index) => {
  if (index >= questions.length) {
    // Handle end of quiz (e.g., show results, navigate to another page, etc.)
    return;
  }

  const question = questions[index];
  document.getElementById('question').innerText = question.question;

  const options = document.getElementsByName('option');
  for (let i = 0; i < options.length; i++) {
    options[i].nextElementSibling.innerText = question.choices[i];
  }

  const nextButton = document.getElementById('nextButton');
  nextButton.disabled = true;
  nextButton.onclick = () => {
    const selectedOption = document.querySelector('input[name="option"]:checked');
    if (selectedOption) {
      userAnswers.push(selectedOption.value);
      showQuestion(++currentQuestionIndex);
    }
  };
};

document.addEventListener('DOMContentLoaded', async () => {
  await loadQuestions();
  showQuestion(currentQuestionIndex);

  const options = document.getElementsByName('option');
  options.forEach((option) => {
    option.addEventListener('change', () => {
      document.getElementById('nextButton').disabled = false;
    });
  });
});



