# App Design

All the text should be in French

## Main menu
There should be a main menu with several options:

- Texte à trous
- Relier les images
- Réinitialiser les scores
- Paramètres
- Quitter



1. Texte à trous
Question Structure
there should be a choice of 4 words that you would drag and drop in the blank of the sentence, it should have a specific animation once you click on validate and it's the correct word, but it should eject the word back into the background when it is not the correct word. For entertaining purposes, the words should be floating around the sentence so the user has to "catch" them.

Feedback: the user fills the blank with drag and drop, upon drag and drop the word should be in the blank, and if it's the correct word it should be green, if it's the wrong word it should be red and then cast back to the original position
Question Types we want multiple choice, true and false, and matching

2. Relier les images
Image Background it should be a png image that i personally put in the assets/images/background/nameOfTheExercise.png, if there is no matching file it should be a white background.

Connection Mechanism
the user should hold left click on the central image, and bring the mouse to the word, that will create a green link with the validation of the exercise in the case of a correct answer, and if not the link goes red and dissapears

Word List:
the words will come from a json that i wrote, in the form of the png path, then the correct word, then the 4 other incorrect words.
Here is an example of the json file:

{
    "image": "assets/images/image_interaction/question1.png",
    "words": {
      "correct": "deux espèces différentes de grenouille",
      "incorrect": [
        "Un mâle et une femelle grenouille",
        "Une grenouille et un crapaud",
        "Une salamandre et une grenouille",
        "Un triton et un tétard"
      ]
    }
  }
  

3. Game Flow and Design
Navigation: there should be a next and previous button

4. User Interface (UI)
User Input: it should only be click or drag and drop, no touch, no voice

Menu and Options: there should be a main 


## Unit tests

### Quizzes with Text and Holes
Cases:
- the user is successfully redirected back to the main menu if the user clicks on the back button
- the user select the right answer, we have a success message and the user is redirected to the next question
- the user selects the wrong answer, we have a failure message and the user has to try again
- the scores are correctly updated when the user selects a right answer
- the scores are correctly updated when the user selects a wrong answer
- all score variables are correctly reset to their initial values when the user clicks on the reset score button