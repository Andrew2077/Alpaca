import pynecone as pc
class alpaca_chat(pc.State):
    _question: str = ""
    _answer: str = ""
    input = ""

    # ** check box for output
    code: bool = False
    code_lang: str = "python"
    input_enable: str = False

    # ** chech for answer
    thinking = False

    # * generation parameters
    temp: float = 2.0
    num_words: int = 45
    #################### UI Changing params #############################
    #TODO : connect them to the ui 
    
    #################### Text Area ###############################
    def set_question(self, question):
        self._question = question

    @pc.var
    def get_question(self):
        return self._question

    ##################### button ################################

    def process_answer(self):
        self.thinking = True

    def get_answer(self):
        #TODO : handle inputs for instsructions 
        # generation_config = GenerationConfig(
        #   temperature = float(float(self.temp) / 10),
        #   top_p=0.75,
        #   top_k=40,
        #   num_beams=4,
        #   max_new_tokens= int(self.num_words))

        # self._answer = response(self._question, generation_config)
        # self._answer = #TODO : change your model
        ## #####################
        self.thinking = False

    @pc.var
    def view_answer(self):
        return self._answer

    ##################### generation parameters ##################

    def code_output(self):
        self.code = not (self.code)


def index():
    return pc.box(
        pc.vstack(
            # * Title
            pc.center(
                pc.heading(
                    "Alpaca-Q/A",
                    font_size="3.5em",
                    _hover={"cursor": "pointer"},
                ),
                padding_bottom="2em",
                width="75%",
                #padding_right="2em",
            ),
            pc.hstack(
                pc.vstack(
                    # * Question spot
                    pc.heading("instruction", font_size="1.5em", align_items="left"),
                    pc.text_area(
                        placeholder="Ask Alpaca",
                        on_blur=alpaca_chat.set_question,
                        width="100%",
                        background="white",
                    ),
                    pc.divider(),
                    pc.cond(
                        alpaca_chat.input_enable,
                        c1=pc.vstack(
                            pc.heading("Input", font_size="1.5em"),
                            pc.text_area(
                                placeholder="input for Question",
                                on_blur=alpaca_chat.set_input,
                                background="white",
                            ),
                            width="100%",
                        ),
                    ),
                    pc.divider(),
                    # * waiting for answer
                    pc.cond(
                        alpaca_chat.thinking,
                        pc.vstack(
                            pc.text("Alpaca is thinking "),
                            pc.progress(is_indeterminate=True, width="75%"),
                        ),
                        # pc.text("Alapaca is done "),
                    ),
                    # * Answer spot
                    pc.cond(
                        alpaca_chat.code,
                        c1=pc.vstack(
                            pc.text("you : " + alpaca_chat.get_question,width="100%",background="white",),
                            pc.text("Alpaca : ",width="100%",background="white",),
                            pc.code_block(alpaca_chat.view_answer,width="100%",language=alpaca_chat.code_lang,),
                            width="100%",background="white",
                        ),
                        c2=pc.vstack(
                            pc.text("you : " + alpaca_chat.get_question, width="100%", background="white"),
                            pc.text("Alpaca : " + alpaca_chat.view_answer, width="100%", background="white"), width="100%", background="white"),
                      ),
                    pc.center(  # * chat button
                        pc.button(
                            "Ask Alpaca",
                            width="100%",
                            on_click=[
                                alpaca_chat.process_answer,
                                alpaca_chat.get_answer,
                            ],
                            background="gray",
                        ),
                    ),
                    pc.accordion(
                        pc.accordion_item(
                            pc.accordion_button(
                                pc.heading("Generation Settings"),
                                pc.accordion_icon(),
                                reduce_motion=True,
                            ),
                            pc.accordion_panel(
                                pc.center(
                                    pc.vstack(
                                        # * unique ability
                                        pc.hstack(
                                            pc.center(
                                                pc.tooltip(
                                                    pc.text(
                                                        f"Tempreture ", font_size=20
                                                    ),
                                                    label="This indicates unique-ability of genereation, set high for relatively close generation",
                                                ),
                                                pc.spacer(),
                                                pc.slider(
                                                    default_value=2,
                                                    on_change=alpaca_chat.set_temp,
                                                    min_=1,
                                                    max_=10,
                                                    width="50%",
                                                ),
                                                width="100%",
                                            ),
                                            width="100%",
                                        ),
                                        # * code output
                                        pc.hstack(
                                            pc.center(
                                                pc.tooltip(
                                                    pc.text(
                                                        "Code Output", font_size=20
                                                    ),
                                                    label="enable to handle generated code correctly",
                                                ),
                                                pc.spacer(),
                                                pc.switch(
                                                    on_change=alpaca_chat.set_code
                                                ),
                                                width="100%",
                                            ),
                                            width="100%",
                                        ),
                                        # * Input enable for instruction like summarize:
                                        pc.hstack(
                                            pc.center(
                                                pc.tooltip(
                                                    pc.text(
                                                        "Instruction's input - Not Working yet",
                                                        font_size=20,
                                                    ),
                                                    label="Enable when your task includes inputs, ex : Summarize ",
                                                ),
                                                pc.spacer(),
                                                pc.switch(
                                                    on_change=alpaca_chat.set_input_enable
                                                ),
                                                width="100%",
                                            ),
                                            width="100%",
                                        ),
                                        # * number of generated words
                                        pc.hstack(
                                            pc.center(
                                                pc.tooltip(
                                                    pc.text(
                                                        "Max number of tokens",
                                                        font_size=20,
                                                    ),
                                                    label="Max Number of generated words",
                                                ),
                                                pc.spacer(),
                                                pc.number_input(
                                                    defaultValue=64,
                                                    on_change=alpaca_chat.set_num_words,
                                                    width="50%",
                                                    background="white",
                                                    max_ = 250,
                                                    min_ = 10,
                                                ),
                                                width="100%",
                                            ),
                                            width="100%",
                                        ),
                                        # * language output horizontal stack
                                        pc.hstack(
                                            pc.center(
                                                pc.tooltip(
                                                    pc.text(
                                                        "code language", font_size=20
                                                    ),
                                                    label="Write the type of language",
                                                ),
                                                pc.spacer(),
                                                pc.input(
                                                    defaultValue="python",
                                                    on_blur=alpaca_chat.set_code_lang,
                                                    width="50%",
                                                    background="white",
                                                ),
                                                # pc.switch(on_change=alpaca_chat.set_code),
                                                width="100%",
                                            ),
                                            width="100%",
                                        ),
                                        pc.alert(
                                            pc.alert_icon(),
                                            pc.alert_title(
                                                "Refresh if it took longer than intended, don't worry, your answer'll be there"
                                            ),
                                            status="warning",
                                        ),
                                    ),
                                    width="100%",
                                ),
                            ),
                        ),
                        width="100%",
                    ),
                    width="100%",
                    padding_bottom="4em",
                ),
                width="80%",
                align_items="bottom",
            ),
            width="100%",
            height="100%",
            padding_top="2em",
            # background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
            # background = 'white',
        ),
        width="100%",
        height="100%",
        padding_top="2em",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


app = pc.App(state=alpaca_chat)
app.add_page(index)
app.compile()
