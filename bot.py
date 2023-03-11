import re
import random

class RuleBot:
    ###  Potential Negative Response
    negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")
    ### Exit conversation Keywords
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
    ### Random questions
    random_questions = (
        "Why are you here? ",
        "Are there many humans like you? ",
        "what do you consume for sustenance? ",
        "Is there intelligent life on this planet? ",
        "Does Earth have a leader? ",
        "What technology do you have on this planet? "
    )

    def __init__(self):
        self.alienbabble = {'describe_planet_internet': r'.*\s*your planet.*',
                            'answer_why_intent': r'why\sare.*',
                            'about_soa': r'.*s\*soa',
                            'about_session': r'.*\s*session'
                            }

    def greet(self):
        self.name = input("What is your name?\n")
        will_help = input(
            f"Hi {self.name}, I am Ai-Bot. Will you help me learn about your planet?\n"
        )
        if will_help in self.negative_responses:
            print("ok, have a nice Earth day!")
            return
        self.chat()

    def make_exit(self, reply):
        for command in self.exit_commands:
            if reply == command:
                print("Okay have a nice Earth day!")
                return True

    def chat(self):
        reply = input(random.choice(self.random_questions)).lower()
        while not self.make_exit(reply):
            reply = input(self.match_reply(reply))

    def match_reply(self, reply):
        for key, value in self.alienbabble.items():
            intent = key
            regex_pattern = value
            found_match = re.match(regex_pattern, reply)
            if found_match and intent == 'describe_planet_intent':
                return self.describe_planet_intent()
            elif found_match and intent == 'answer_why_intent':
                return self.answer_why_intent()
            elif found_match and intent == 'about_soa':
                return self.about_soa()
            elif found_match and intent == 'about_session':
                return self.about_session()
        if not found_match:
            return self.no_match_intent()

    def describe_planet_intent(self):
        response = ("My plannet is a utopia of diverse organisms and species. \n",
                    "I am from Opidipus, the capital of the wayward Galaxies\n")
        return random.choice(response)

    def answer_why_intent(self):
        responses = ("I come in peace\n", "I am here to collect data on your plannet and its inhabitants\n",
                     "I heared the coffee is good\n")
        return random.choice(responses)

    def about_soa(self):
        responses = ("SOA is a largest proffessional educational institution\n",
                     "SOA is where your career and skill grows\n")
        return "SOA is a great place to learn"

    def about_session(self):
        responses = ('Session is on 14th Aug 2022\n', 'Session was Cool!!')
        return random.choice(responses)

    def no_match_intent(self):
        responses = (
        "Please tell me more.\n", "Tell me more!\n", "Why do you say that?\n", "I see . Can you elaborate?\n",
        "Interesting. Can you tell me more?\n", "I see. How do you think?\n", "Why?\n",
        "How do you think I feel when you say that?\n"
        )
        return random.choice(responses)


AiBot = RuleBot()
AiBot.greet()
