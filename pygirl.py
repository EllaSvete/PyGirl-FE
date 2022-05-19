from pyodide.http import pyfetch
import asyncio
import string

# TODO: Render the snake

pyscript = pyscript  # wierd, but gets rid of many linter warnings

url = "https://text-of-fortune.vercel.app/api/tof"
# url = "http://localhost:3000/api/tof"

game_data = None # fetch this data from back end

prompts = {
    "start": "Guess a letter to solve the word",
    "incorrect": "Wrong!!! Guess Again",
    "correct": "Noice! Keep it up",
    "victory": "Congratulations",
    "defeat": "You'll do better next time"
}


async def fetch_game_data(query_string=""):
    global game_data

    # ?id = 1 & guess = f & guesses = xy
    response = await pyfetch(url=url + query_string, method="GET")

    game_data = await response.json()

    id_ = game_data["id"]
    unsolved_word = game_data["working_word"]
    status = game_data["status"]
    guesses = game_data["guesses"]

    prompt = prompts[status]

    incorrect_guesses = ""
    for guess in guesses:
        if guess not in unsolved_word:
            incorrect_guesses += guess

    tries_left = 6 - len(incorrect_guesses)

    incorrect_guesses = incorrect_guesses or "***"

    render_game_info(id_, prompt, unsolved_word, incorrect_guesses, tries_left)

    render_buttons(guesses)


def render_game_info(id_, prompt, unsolved_word, incorrect_guesses, tries_left):
    pyscript.write("game-id", id_)
    pyscript.write("prompt", prompt)
    pyscript.write("unsolved-word", unsolved_word)
    pyscript.write("incorrect-guesses", incorrect_guesses)
    pyscript.write("tries-left", tries_left)
    snake_texts = [
            "",
            "xxxx -=: xxxxx<br>",
            """        ________
                \nxxxx -=:___________  xxxxx """,
            """         ________/   /
                \nxxxx -=:___________/ xxxxx """,
            """
                    \\
                        \    /
                ________/   /
        xxxx -=:___________/ xxxxx""",
            """        _____
                    /  0 0 \\
                    \\
                        \    /
                ________/   /
        xxxx -=:___________/ xxxxx
        """,
            """        _____
                     /  0 0 \\
                    \    --------<
                        \    /
                ________/   /
        xxxx -=:___________/ xxxxx
        """
        ]
    
    error_count = 6 - tries_left
    snake_message = snake_texts[error_count]
  
    # if tries_left == 6:
    #   return snake_texts[0] 
    # if tries_left == 5:
    #   return snake_texts[1]
    # if tries_left == 4:
    #   return snake_texts[2] 
    # if tries_left == 3:
    #   return snake_texts[3]
    # if tries_left == 2:
    #   return snake_texts[4] 
    # if tries_left == 1:
    #   return snake_texts[5]
    # if tries_left == 0:
    #   return snake_texts[6]

    pyscript.write("snake_images", snake_message)



def render_buttons(guesses):
    """
    Go through alphabet and make button for any unused letters
    :param guesses:
    :return:
    """

    top_row = "QWERTYUIOP"
    middle_row = "ASDFGHJKL"
    bottom_row = "ZXCVBNM"

    button_markup = ""

    for char in top_row:
        if char not in guesses:
            button_markup += f"<button class='px-2'>{char}</button>"
    pyscript.write("button_row1", button_markup)

    button_markup = ""
    for char in middle_row:
        if char not in guesses:
            button_markup += f"<button class='px-2'>{char}</button>"
    pyscript.write("button_row2", button_markup)

    button_markup = ""
    for char in bottom_row:
        if char not in guesses:
            button_markup += f"<button class='px-2'>{char}</button>"
    pyscript.write("button_row3", button_markup)


async def clickHandler(event):
    id_ = game_data["id"]
    guess = event.target.textContent # a or b or z
    guesses = game_data["guesses"]
    guess = guess.lower()
    query_params = f"?id={id_}&guess={guess}&guesses={guesses}"

    await fetch_game_data(query_params)


fetch_game_data()
