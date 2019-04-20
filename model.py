import json
from collections import defaultdict


class Model:
    def __init__(self, model, questions):
        self.raw_model = json.loads(open(model, 'r').read())
        self.questions = json.loads(open(questions, 'r').read())
        self.objects_prob = {x: 0 for x in self.raw_model}
        self.words_value, self.words_prob, self.negate_words_value = self.__calculate_word_weight()
        self.objects_dict = self.__set_2d_object_dict()
        self.highest_word_value = self.get_the_highest_word_value()
        self.iteration = 0
        self.suggested_question = {}
        self.minimum_threshold = 0.7

    def __calculate_word_weight(self):
        total_words = 0
        words_value = defaultdict(float)
        words_prob = {}
        n_words_value = {}

        for data in self.raw_model.values():
            for i in data:
                total_words += 1
                words_value[i] += 1

        for i, value in words_value.items():
            words_value[i] = 1 / value
            words_prob[i] = value / total_words
            n_words_value[i] = 1 / (total_words - value)

        return words_value, words_prob, n_words_value

    def __set_2d_object_dict(self):
        object_dict = {}
        for key, data in self.raw_model.items():
            words_dict = {}
            for i in data:
                words_dict[i] = True
            object_dict[key] = words_dict

        return object_dict

    def get_the_highest_word_value(self):
        return max(self.words_prob, key=self.words_prob.get)

    def reset_dynamic_calculation(self):
        self.objects_prob = {x: 0 for x in self.raw_model}
        self.suggested_question = {}
        self.iteration = 0

    def calculate_probability(self, word, correct):
        self.iteration += 1
        self.suggested_question[word] = True

        prob = self.words_value[word] if correct else self.negate_words_value[word]

        for key, val in self.objects_dict.items():
            temp = self.objects_prob[key] * (self.iteration - 1)
            if (word in self.objects_dict[key] and correct) or (word not in self.objects_dict[key] and not correct):
                self.objects_prob[key] = (temp + prob) / self.iteration
            else:
                self.objects_prob[key] = temp / self.iteration

        max_o = max(self.objects_prob, key=self.objects_prob.get)
        for i in self.raw_model[max_o]:
            if i not in self.suggested_question:
                return i, None

        if self.objects_prob[max_o] < self.minimum_threshold:
            return None, None

        return None, max_o
