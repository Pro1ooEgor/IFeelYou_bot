def return_text_by_filepath(path):
    with open(path) as f:
        return f.read()


opinions = {
    'клево': {
        'description': {
            'len': 4,
            1: ['спокойно', 'наслаждение', 'весело', 'блаженство', 'удовольствие', 'удовлетворение', 'легко'],
            2: ['любопытно', 'влечение', 'интересно', 'вожделение', 'позыв', 'вдохновение', 'стремлюсь'],
            3: ['мило', 'симпатия', 'по-доброму', 'обожаю', 'тепло на душе', 'принятие', 'нежность'],
            4: ['другое'] * 7,
        },
        'state_is': {
            'len': 4,
            1: ['поддержка', 'информация', 'забота', 'запасной план', 'полезность', 'разнообразие', 'деньги',
                'эффективность', 'план действий', 'достоверные источники', 'доверие', 'авторитетное мнение',
                'стабильность', 'развитиеуверенность'],
            2: ['близость', 'чувства', 'внимание', 'индивидуальность', 'красота', 'привилегии', 'творчество',
                'признание', 'похвала', 'искренность', 'благодарность', 'восхищение', 'связь', 'привлекательность'],
            3: ['власть', 'преданность', 'сила', 'честь', 'возможность противостоять', 'ответственность',
                'профессионализм', 'справедливость', 'возможность оказать сопротивление', 'автономность',
                'однозначность', 'свобода', 'независимость', 'достижения'],
            4: ['другое'] * 14,
        },
        'wants': {
            1: 'безопасности',
            2: 'любви',
            3: 'уважения',
        },
    },
    'не очень': {
        'description': {
            'len': 6,
            1: ['скучно', 'горюю', 'апатия', 'грусть', 'счастья нет', 'печальненько', 'расстройство'],
            2: ['стремно', 'беспокойство', 'волнение',   'ужас', 'тревожненько', 'растерянность', 'паника'],
            3: ['мерзко', 'тошниловка', 'отвращение', 'гадко', 'антипатия', 'брезгую', 'отторжение'],
            4: ['бесит', 'я протестую', 'сейчас порву', 'недоволен', 'я в ярости', 'гневаюсь', 'злюсь'],
            5: ['чувствую себя нелепо', 'позор мне', 'ущербность', 'некчемность', 'стесняюсь', 'смущаюсь', 'неловко'],
            6: ['другое'] * 7,
        },
        'state_is': {
            'len': 4,
            1: ['поддержка', 'информация', 'забота', 'запасной план', 'полезность', 'разнообразие', 'деньги', 'эффективность', 'план действий', 'достоверные источники', 'доверие', 'авторитетное мнение', 'стабильность', 'развитиеуверенность'],
            2: ['близость', 'чувства', 'внимание', 'индивидуальность', 'красота', 'привилегии', 'творчество', 'признание', 'похвала', 'искренность', 'благодарность', 'восхищение', 'связь', 'привлекательность'],
            3: ['власть', 'преданность', 'сила', 'честь', 'возможность противостоять', 'ответственность', 'профессионализм', 'справедливость', 'возможность оказать сопротивление', 'автономность', 'однозначность', 'свобода', 'независимость', 'достижения', 'личные границы'],
            4: ['другое'] * 14,
        },
        'wants': {
            1: 'безопасности',
            2: 'любви',
            3: 'уважения',
        },
        'my_advices': {
            'len': 5,
            1: return_text_by_filepath('advices/my/1.txt'),
            2: return_text_by_filepath('advices/my/2.txt'),
            3: return_text_by_filepath('advices/my/3.txt'),
            4: return_text_by_filepath('advices/my/4.txt'),
            5: return_text_by_filepath('advices/my/5.txt'),
        },
        'partner_advices': {
            'len': 5,
            1: return_text_by_filepath('advices/partner/1.txt'),
            2: return_text_by_filepath('advices/partner/2.txt'),
            3: return_text_by_filepath('advices/partner/3.txt'),
            4: return_text_by_filepath('advices/partner/4.txt'),
            5: return_text_by_filepath('advices/partner/5.txt'),
        },
    },
}
another_form_words = {

}