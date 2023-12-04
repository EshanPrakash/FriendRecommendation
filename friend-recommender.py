#!/usr/bin/env python3


class SocialNetwork:

    def __init__(self):
        '''Constructor; initialize an empty social network
        '''
        self.users = {}

    def list_users(self):
        '''List all users in the network

        Returns:
            [str]: A list of usernames
        '''

        return list(self.users.keys())


    def add_user(self, user):
        '''Add a user to the network

        This user will have no friends initially.

        Arguments:
            user (str): The username of the new user

        Returns:
            None
        '''

        if user not in self.users.keys():
            self.users[user] = []

        pass # FIXME

    def add_friend(self, user, friend):
        '''Adds a friend to a user

        Note that "friends" are one-directional - this is the equivalent of
        "following" someone.

        If either the user or the friend is not a user in the network, they
        should be added to the network.

        Arguments:
            user (str): The username of the follower
            friend (str): The username of the user being followed

        Returns:
            None
        '''

        if user not in self.users.keys():
            self.add_user(user)
        if friend not in self.users.values():
            self.add_user(friend)
        self.users[user].append(friend)

        pass # FIXME

    def get_friends(self, user):
        '''Get the friends of a user

        Arguments:
            user (str): The username of the user whose friends to return

        Returns:
            [str]: The list of usernames of the user's friends

        '''

        friendlist = []

        for i in enumerate(self.users.items()):
            #print(i[1][0])
            if i[1][0] == user:
                friendlist = i[1][1]

        return friendlist

    def suggest_friend(self, user):
        '''Suggest a friend to the user

        See project specifications for details on this algorithm.

        Arguments:
            user (str): The username of the user to find a friend for

        Returns:
            str: The username of a new candidate friend for the user
        '''

        '''
         1. Find another user that is the most similar to the specified user, based on the Jaccard index of their friends. 
         2. Out of the most-similar-user's friends, find the one with the most followers that the specified user does not already follow.
        '''
        most_similar_user = ""
        #user = "francis"
        user_friends = []
        not_user_friends = []
        most_similar_user_friends = []
        oldjaccard = 0
        recommended_friend = ""

        for i in enumerate(self.users.items()):
            if i[1][0] == user:
                user_friends = i[1][1]

        for i in enumerate(self.users.items()):
            if i[1][0] != user:
                not_user_friends = i[1][1]

            #print(user_friends)
            #print(not_user_friends)

            intersection = len(list(set(user_friends).intersection(not_user_friends)))
            union = (len(user_friends) + len(not_user_friends)) - intersection
            newjaccard = float(intersection) / union
            #print("New Jaccard for " + str(i[1][0]) + ": " + str(newjaccard))
            if newjaccard > oldjaccard:
                most_similar_user = i[1][0]
                oldjaccard = newjaccard
            #print("Old Jaccard " + str(most_similar_user) + ": " + str(oldjaccard))

        for i in enumerate(self.users.items()):
            if i[1][0] == most_similar_user:
                most_similar_user_friends = i[1][1]

        unique_user_friends = list(set(user_friends) - set(most_similar_user_friends))
        unique_most_similar_user_friends = list(set(most_similar_user_friends) - set(user_friends))

        result = unique_user_friends + unique_most_similar_user_friends


        #print(user)
        #print(most_similar_user)
        #print(user_friends)
        #print(most_similar_user_friends)
        #print(result)
        #print()
        oldcount = 0
        for i in result:
            for person in enumerate(self.users.items()):
                if i == person[1][0]:
                    person_friends = person[1][1]
                    #print(person_friends)
                    for friend in person_friends:
                        newcount = sum(friend in friends_list for friends_list in self.users.values())
                        #print(newcount)
                        if newcount > oldcount:
                            oldcount = newcount
                            recommended_friend = friend
                            #print(recommended_friend)
                        #print(oldcount)
                        #counts[friend] = count
                        #print(f"{friend}: {count} times")
                        #for person1 in enumerate(self.users.values()):
                        #    print(person1[1])

                    #for index in person_friends:
                    #    print(index)
                    #    for person1 in enumerate(self.users.items()):
                    #        if index == person1[1][0]:
                    #            print(len(person1[1][1]))

        return recommended_friend

    def to_dot(self):
        result = []
        result.append('digraph {')
        result.append('    layout=neato')
        result.append('    overlap=scalexy')
        for user in self.list_users():
            for friend in self.get_friends(user):
                result.append('    "{}" -> "{}"'.format(user, friend))
        result.append('}')
        return '\n'.join(result)


def create_network_from_file(filename):
    '''Create a SocialNetwork from a saved file

    Arguments:
        filename (str): The name of the network file

    Returns:
        SocialNetwork: The SocialNetwork described by the file
    '''
    network = SocialNetwork()
    with open(filename) as fd:
        for line in fd.readlines():
            line = line.strip()
            users = line.split()
            network.add_user(users[0])
            for friend in users[1:]:
                network.add_friend(users[0], friend)
    return network


def main():
    network = create_network_from_file('simple.network')
    print(network.to_dot())
    print(network.suggest_friend('francis'))


if __name__ == '__main__':
    main()
