#!/usr/bin/env python3

def main():
    with open('06.in') as input:
        for line in input.read().splitlines():
            message = list(line)
            for end in range(4, len(message)):
                start_of_packet = message[end - 4:end]
                if len(set(start_of_packet)) == len(start_of_packet):
                    print(end)
                    break
            for end in range(14, len(message)):
                start_of_message = message[end - 14:end]
                if len(set(start_of_message)) == len(start_of_message):
                    print(end)
                    break
            

__name__ == "__main__" and main()
