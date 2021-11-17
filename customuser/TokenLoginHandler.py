import secrets
import os
import logging
import logging.handlers
import time


class TokenLoginHandler:

    # initialize the class with a dictionary of tokens, and a path to the text file containing the tokens and dictionary keys
    def __init__(self):
        self.tokens = {}
        self.token_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token_file.txt')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
    
    # a function that reads in a string, and generates a token and adds it to the dictionary
    def generate_token(self, username):
        sw = time.time()
        #check if the username is in the token_file.txt
        #if it is, reutrn the token
        #if it is not, generate a token, add it to the dictionary, and write the dictionary to the file
        token = self.read_token_from_file(username)
        if token:
            self.tokens[username] = token
            self.logger.info('Found token for user: ' + username + ' in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms' + ', at ' + str(time.ctime()))
            return token
        else:
            token = secrets.token_urlsafe(16)
            self.tokens[username] = token
            self.write_token_to_file()
            self.logger.info('Generated token for user: ' + username + ' in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms' + ', at ' + str(time.ctime()))

    #A function that takes the dictionary, and adds the username and token to the text file in the format username:token while also keeping excisting tokens in the file
    def write_token_to_file(self):
        sw = time.time()
        with open(self.token_file_path, 'a') as f:
            for key, value in self.tokens.items():
                #format key string to be all lowercase and no spaces
                key = key.lower().replace(' ', '')
                #keep every item in the file, but add the new item keeping history
                f.write(key + ':' + value + '\n')
                self.logger.info('Wrote tokens to file in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms' + ', at ' + str(time.ctime()))

    #A function that reads in a username, and determines if the username is in the token_file.txt, and if it is, returns the token. without the token, the user will not be able to login
    #without using the dictionary
    def read_token_from_file(self, username):
        sw = time.time()
        #handle if it's a nontype username
        if not isinstance(username, str):
            #convert to string
            username = str(username)
        username = username.lower().replace(' ', '')
        with open(self.token_file_path, 'r') as f:
            for line in f:
                if username in line and len(username) == len(line[:line.find(':')]):
                    token = line.split(':')[1].strip()
                    self.logger.info('Read token from file for user: ' + username + ', at ' + str(time.ctime()) + ' in ' + str(round((time.time() - sw) * 1000, 4)) + ' ms')
                    return token
        self.logger.info('User not found in file (' + username + ') at ' + str(time.ctime()))
        return None
    # a simple boolean function for user creation handling
    def token_found_compute(self, username):
        token = self.read_token_from_file(username)
        if token:
            return True
        else:
            return False


#test this class
def main():
    tlh = TokenLoginHandler()
    tlh.generate_token('test')
    print(tlh.tokens)
    print(tlh.read_token_from_file('test'))
    tlh.generate_token('TestingUser')
    tlh.generate_token('newtestinguser')

if __name__ == '__main__':
    main()
    


