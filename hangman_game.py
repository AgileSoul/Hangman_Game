def get_adjectives_dictionary():
    """ 
        open and read adjectives file

        returns dictionary with file data
    """

    with open('./files/adjectives.txt', 'r', encoding='utf-8') as file:
        """ i did it with dictionary comprehensions, but i believe that this code is not scalable:
            import re
            regex = re.compile('(?i)^([a-z]+):\s(.+\.)\n$')
            adjectives_dictionary = {re.match(regex, line).group(1): re.match(regex, line).group(2) for line in file}
        """
        import re
        regex_pattern = re.compile(': ')

        def get_key_value(line):
            """ list with key and value of file data """
            key_value = re.split(regex_pattern, line, 1)
            assert key_value[0] != line, 'Fail to create key_value_list'

            key_value[1] = key_value[1].replace('\n', '')
            
            return tuple(key_value)
        
        adjectives_dictionary = dict(map(get_key_value, file))
        
    file.close()

    return adjectives_dictionary 

def get_random_adjective(dictionary):
    """
        dictionary dict any dict
        
        returns a random value from dictionary
    """
    assert isinstance(dictionary, dict), 'Parameter dictionary is not dict'

    from random import choice
    random_adjective = choice(list(dictionary.items()))

    return random_adjective

def show_principal_view(random_adjective):
    """ 
        Print the principal view of program

        adjective string any adjective
    """
     
    from os import system

    operatives_systems = {
        'Linux' : 'clear',
        'Darwin' : 'clear',
        'Windows' : 'cls'
    }
    
    adjective = random_adjective[0]
    adjective_meaning = random_adjective[1]
    
    def get_operative_system():
        from platform import system as so
        return so()
    
    def clear_screen(operative_system):
        operative_system = operatives_systems.get(operative_system, 'clear')
        system(operative_system)

    def replace_hidden_adjective(letter, adjective, start_index, hidden_adjective):
        if letter in adjective[start_index:]:
            index = adjective.index(letter, start_index)
            start_index = index + 1
            """
            letter : e ; e
            adjective : 'clever'; 'clever'
            index : 2 ; 4
            start_index : 3 ; 5
            hidden_adjective : '{"__"}{"e"}{'___'}'; '{'__e_'}{'e'}{'_'}'
            """
            hidden_adjective = f'{hidden_adjective[:index]}{letter}{hidden_adjective[start_index:]}'
            hidden_adjective = replace_hidden_adjective(letter, adjective, start_index, hidden_adjective)

        return hidden_adjective

    def print_header(hidden_adjective, adjective_meaning, help_bool, attempts, warning_advise):
        get_centered_text = lambda text, center_length = 65, separator = ' ': text.center(center_length, separator)
        
        def print_title():
            title_characters = 65
            title = get_centered_text(' Hangman Game  ',center_length = title_characters, separator='-')
            print('=' * (title_characters + 2))
            print('=' + title + '=')
            print('=' * (title_characters + 2)) 

        def print_help(adjective_meaning, help_bool):
            help_characters = 67
            help_advise = get_centered_text(f' If you want help type [ --help ] ', help_characters - 2, ' ')
            adjective_meaning = get_centered_text(adjective_meaning[:help_characters - 2], help_characters - 2)
            print('—' * help_characters) 
            print('|' + help_advise + '|')
            if help_bool:
                help_literal = get_centered_text('Help:', help_characters - 2)
                print(f'|{help_literal}|')
                print(f'|{adjective_meaning}|')
            print('—' * help_characters) 
        
        def print_attempts(attempts):
            attempts_characters = 67
            attempts_text = get_centered_text(f'Attempts: {attempts}', attempts_characters - 2)
            print('—' * attempts_characters)
            print(f'|{attempts_text}|')
            print('—' * attempts_characters)

        def print_hidden_adjective(hidden_adjective):
            hidden_adjective_characters = 67
            hidden_adjective = ' '.join(letter for letter in hidden_adjective)
            hidden_adjective = get_centered_text(hidden_adjective)
            print('+' * hidden_adjective_characters)
            print('+' + ' ' * (hidden_adjective_characters - 2) + '+')
            print('+' + hidden_adjective + '+')
            print('+' + ' ' * (hidden_adjective_characters - 2) + '+')
            print('+' * hidden_adjective_characters)

        def print_warning_advise(warning_advise):
            if warning_advise[0]:
                print(f'Warning: {warning_advise[1]}')

        clear_screen(operative_system)
        print_title()
        print_help(adjective_meaning, help_bool)
        print_attempts(attempts)
        print_hidden_adjective(hidden_adjective)
        print_warning_advise(warning_advise)
        print()

    assert isinstance(adjective[0], str), 'Parameter adjective[0] is not str'
    assert len(adjective[0]) > 0, 'Len adjective[0] is not positive'
    
    operative_system = get_operative_system()
    hidden_adjective = '_' * len(adjective) 
    help_bool = False
    warning_advise = [ False, ]
    attempts = 0

    while (hidden_adjective != adjective) and (attempts < 5) :
        print_header(hidden_adjective, adjective_meaning, help_bool, attempts, warning_advise)
        letter = input(f'Enter a letter: ').lower()

        try:
            if letter == '--help':
                help_bool = not help_bool
                continue
            elif len(letter) != 1:
                raise ValueError('Characters Length Error: You must type a single character')
            elif not letter.isalpha():
                raise ValueError('Character not alphabetic: You should type an alphabetic character')
        except ValueError as ve:
            advise = str(ve).split(': ', 1)[1]
            warning_advise = [ True, advise ]
            continue
        
        warning_advise = [ False, ]
        
        old_hidden_adjective = hidden_adjective
        hidden_adjective = replace_hidden_adjective(letter, adjective, 0, hidden_adjective)
        if old_hidden_adjective == hidden_adjective:
            attempts += 1

    print_header(hidden_adjective, adjective_meaning, help_bool, attempts, warning_advise)
    if attempts < 5:
        print(f'You win, the win word is [ {adjective.upper()} ]')
    else:
        print(f'You lose :(, the win word was [ {adjective.upper()} ]')
    
    print()

def run():
    adjectives_dictionary = get_adjectives_dictionary()
    play_again = ''
    while True:
        random_adjective = get_random_adjective(adjectives_dictionary)
        show_principal_view(random_adjective)
        while not (play_again.lower() in ('yes', 'y', 'not', 'no', 'n')):
            play_again = input('Do you want play again? [ yes/not ]: ')
        if play_again.lower() in ('yes', 'y'):
            play_again = ''
            continue
        else:
            break
    
    print()

if __name__ == '__main__':
    run()
