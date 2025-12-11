document.addEventListener("DOMContentLoaded", () => {
    //Variables
    let questions = [];
    let currentQuestion = 0;
    let time = 10;
    let timerId;
    let score = 0;
    const pickedAnswers = [];
    //Dom
    const quizBox = document.getElementById("quizmodel");
    const qText = document.getElementById("quizquestion");
    const optionsBox = document.getElementById("optionscontainer");
    const feedback = document.getElementById("quizfeedback");
    const nextBtn = document.getElementById("button");
    const timeText = document.getElementById("timeleft");
    //Fetch quiz data
    const loadQuiz = async () => {
        try {
            const res = await fetch("http://localhost:5000/seed_quiz");
            const data = await res.json();
            console.log("got data:", data);

            if (data.questions) {
                questions = data.questions.slice(0, 5);
            } else {
                alert("No questions received");
                return;
            }
            quizBox.style.display = "flex";
            showQuestion();
            startTimer();
        } catch (err) {
            console.error("Error loading quiz:", err);
            alert("Error loading quiz");
        }
    };
    //Show the question\\
    const showQuestion = () => {
        const q = questions[currentQuestion];
        if (!q) return;
        const keys = Object.keys(q.choices).sort();
        const opts = keys.map(key => q.choices[key]);

        q.correctIndex = keys.indexOf((q.correct_choice || "").toUpperCase());

        time = 10;
        feedback.textContent = "";
        optionsBox.innerHTML = "";
        nextBtn.style.display = "none";
        qText.textContent = q.question;
        opts.forEach((opt, idx) => {
            const div = document.createElement("div");
            div.className = "option";
            div.textContent = opt;
            div.addEventListener("click", () => pickAnswer(idx));
            optionsBox.appendChild(div);
        });
    };
    //Start the timer\\
    const startTimer = () => {
        clearInterval(timerId);
        timeText.textContent = time;
        timerId = setInterval(() => {
            time -= 1;
            timeText.textContent = time;

            if (time <= 0) {
                clearInterval(timerId);
                feedback.textContent = "Time up";
                pickedAnswers[currentQuestion] = null;
                [...optionsBox.children].forEach(item => item.style.pointerEvents = "none");
                nextBtn.style.display = "block";
            }
        }, 1000);
    };
    //Pick an answer\\
    const pickAnswer = (idx) => {
        clearInterval(timerId);
        pickedAnswers[currentQuestion] = idx;

        const q = questions[currentQuestion];
        if (idx === q.correctIndex) score += 1;
        [...optionsBox.children].forEach((item, i) => {
            item.style.pointerEvents = "none";
            if (i === idx) {
                item.style.backgroundColor = (i === q.correctIndex) ? "lightgreen" : "pink";
            }
        });
        nextBtn.style.display = "block";
    };
    nextBtn.addEventListener("click", () => {
        currentQuestion++;
        if (currentQuestion >= questions.length) {
            showResults();
        } else {
            showQuestion();
            startTimer();
        }
    });
    //Show the results\\
    const showResults = () => {
        clearInterval(timerId);
        const timerDiv = document.querySelector(".timer");
        if (timerDiv) timerDiv.style.display = "none";
        
        qText.textContent = `Score: ${score} / ${questions.length}`;
        optionsBox.innerHTML = "";
        nextBtn.style.display = "none";

        questions.forEach((q, i) => {
            const div = document.createElement("div");
            div.className = "result-block";

            const h = document.createElement("h3");
            h.textContent = `${i + 1}. ${q.question}`;
            div.appendChild(h);

            const ul = document.createElement("ul");

            const liCorrect = document.createElement("li");
            liCorrect.textContent = `${q.choices[Object.keys(q.choices).sort()[q.correctIndex]]} (correct)`;
            ul.appendChild(liCorrect);

            if (pickedAnswers[i] !== q.correctIndex && pickedAnswers[i] !== null) {
                const liWrong = document.createElement("li");
                liWrong.textContent = `${q.choices[Object.keys(q.choices).sort()[pickedAnswers[i]]]} (yours)`;
                ul.appendChild(liWrong);
            }

            div.appendChild(ul);
            optionsBox.appendChild(div);
        });
        
        // Store score in sessionStorage before redirecting
        sessionStorage.setItem("quizScore", JSON.stringify({
            score: score,
            total: questions.length
        }));
        // Don't send score here - final_window.js will send the combined score
        window.location.href = "../views/final_window.html"
    };    
    loadQuiz();
});