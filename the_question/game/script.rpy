# Declare characters used by this game.
define s = Character(_("Sylvie"), color="#c8ffc8")
define m = Character(_("Me"), color="#c8c8ff")

# This is a variable that is True if you've compared a VN to a book, and False
# otherwise.
default book = False

# The game starts here.
label start:

    scene bg uni
    show sylvie green smile

    "I've known Sylvie since we were kids. She's got a big heart and she's always been a good friend to me."

    "But recently... I've felt that I want something more."

    "More than just talking, more than just walking home together when our classes end."

    s "Hi Sharat! Are you going home now? Wanna walk back with me?"

    m "Sure!"

    scene bg meadow
    with fade

    "After a short while, we reach the meadows just outside the neighborhood where we both live."

    "It's a scenic view I've grown used to. Autumn is especially beautiful here."

    m "Hey... Umm..."

    show sylvie green smile
    with dissolve

    "She turns to me and smiles. She looks so welcoming that I feel my nervousness melt away."

    "I'll ask her...!"

    show sylvie green smile

    python: 
        # Import the message function
        from ai import message 

        # Define a variable that will store the eventual label which the plot jumps to.
        label = None 

        # Define a variable that will store the messages between the player and the visual novel character
        messages = []

        # Define a list of possible labels that the plot can jump to.
        possible_labels = ["too fast", "just nice"]

        # Define a list of possible images that the language model can choose to pair with the conversation
        possible_images = ["sylvie blue giggle", "sylvie blue surprised"]

        # Provide some context for the character that the player is interacting with. Refer to the player as 'user' 
        character_profile = "You are Sylvie and you have a slight romantic crush on the user. You are interested in taking the relationship to the next level but you are a bit scared of moving too fast. Depending on how the user phrases his question, you have to make a decision on whether things are moving too fast." 

        # Provide a prompt for the player to respond to 
        prompt = "How will you hint at a romantic relationship with Sylvie?" 


        prompt_messages_list = [prompt]
        # The visual novel character will start a dynamic conversation with the player until a a label is assigned to the conversation. The most appropriate image will also be chosen based on the state of the conversation
        while not label: 

            # User must input something
            user_input = renpy.input(prompt, length=500).strip()
            if not user_input:
                continue

            image, label, messages, prompt_messages_list = message(
                character_profile,
                prompt_messages_list,
                user_input, 
                messages, 
                possible_images,
                possible_labels
            ) 
            renpy.show(image)

            if prompt_messages_list:
                prompt = prompt_messages_list[-1]

                for p in prompt_messages_list[:-1]:
                    renpy.say(s, p)

    # Jump to the associated label based on the the result of the message function
    if label == "too fast": 
        jump too_fast 
    elif label == "just nice": 
        jump just_nice

label just_nice:

    show sylvie green giggle

    "Sylvie did not answer my question directly but she looks visibly happy."

    scene black
    with dissolve

    "From the day onwards, we became closer and closer."

    "And one day..."

    show sylvie blue normal
    with dissolve

    s "Hey..."

    m "Yes?"

    show sylvie blue giggle

    s "Will you marry me?"

    m "What? Where did this come from?"

    show sylvie blue giggle

    s "I know you're the indecisive type. If I held back, who knows when you'd propose?"

    show sylvie blue normal

    s "So will you marry me?"

    m "Of course I will! I've actually been meaning to propose, honest!"

    scene black
    with dissolve

    "We get married shortly after that."

    "Together, we live happily ever after even now."

    "{b}Good Ending{/b}."

    return

label too_fast:

    show sylvie green surprised

    "Sylvie looks visibly shocked by my response."

    "I'm not sure what to do now."

    "I think I will just run away now."

    "{b}Bad Ending{/b}."

    return
