import user_table_file as user
import group_table_file as group
import undelivered_messages_file as undelivered
import FUNCTIONS


DASHED_LINE="\033[91m"+"--------------------"+"\033[0m"

print("Hello! Welcome to FastChat! We emulate a service that was used in the 1980s, probably. Enjoy!")
print(DASHED_LINE, end="\n")
while True:
    print("\nPlease choose the action you want to perform:")
    print(DASHED_LINE)
    print("0: Exit")
    print("1: Sign Up")
    print("2: Log In")
    print(DASHED_LINE)

    choice=input()
    if choice!="0" and choice!="1" and choice!="2":
        print("Invalid choice! Please try again.")
        continue
    elif choice=="0":
        break
    elif choice=="1":
        user_ID_exists=True
        while user_ID_exists:
            print(DASHED_LINE)
            print("You will now need to type in a User ID, which will be displayed to everyone you chat with.\nYou will also need it to log in again.")
            print("\nEnter a unique User ID:")
            ID_input=input()
            print(DASHED_LINE)
            user_ID_exists=FUNCTIONS.check_user_exists(ID_input)
            if user_ID_exists:
                print("\nInvalid entry. User ID already exists!\n")
        
        print("Enter a password:")
        password_input=input()
        print(DASHED_LINE)

        FUNCTIONS.add_user(ID_input, password_input)
        print("\nUser Created! Please log in through your recently created log-in credentials now.")
        
    elif choice=="2":
        print(DASHED_LINE)
        print("Enter your User ID")
        ID_input=input()
        print(DASHED_LINE)
        print("Enter your password:")
        password_input=input()
        print(DASHED_LINE)
        user_credentials_correct=FUNCTIONS.check_user_password(ID_input, password_input)
        if not user_credentials_correct:
            print("Incorrect log-in details entered")
            continue
        FUNCTIONS.set_user_online(ID_input)
        print("You are now logged in! Congratulations! Really, from the bottom of our hearts. You made it to this point.")
        while True:
            print("\nPlease choose the action you want to perform:\n")
            print(DASHED_LINE)
            print("0: Log Out")
            print("1: Send a message to a fellow user")
            print("2: Create a group")
            print("3: Log in to a group as an admin")
            print("4: Send a message to a group")
            print(DASHED_LINE)

            login_choice=input()
            if login_choice!="0" and login_choice!="1" and login_choice!="2" and login_choice!="3" and login_choice!="4":
                print("Invalid choice! Please try again.")
                continue
            elif login_choice=="0":
                print("Thanks for visiting!")
                FUNCTIONS.set_user_offline(ID_input)
                break
            elif login_choice=="1":
                print(DASHED_LINE)
                print("0: Back")
                print("1: Send a text")
                print("2: Send an image")
                print(DASHED_LINE)
                
                message_choice=input()
                if message_choice not in ["0", "1", "2"]:
                    print("Invalid choice! Please try again.")
                    continue
                elif message_choice=="0":
                    continue
                elif message_choice=="1":
                    print(DASHED_LINE)
                    print("Enter your message:")
                    cur_message=input()
                    print(DASHED_LINE)
                    print("Enter the User ID of the receiver:")
                    cur_receiver=input()
                    print(DASHED_LINE)
                    FUNCTIONS.send_text(ID_input, cur_receiver, cur_message)
                    print("Message sent!")
                elif message_choice=="2":
                    print(DASHED_LINE)
                    print("Enter your image directory:")
                    cur_image=input()
                    print(DASHED_LINE)
                    print("Enter the User ID of the receiver:")
                    cur_receiver=input()
                    print(DASHED_LINE)
                    FUNCTIONS.send_image(ID_input, cur_receiver, cur_image)
                    print("Message sent!")
            elif login_choice=="2":
                group_ID_exists=True
                while group_ID_exists:
                    print(DASHED_LINE)
                    print("Enter a unique Group ID:")
                    GroupID_input=input()
                    print(DASHED_LINE)
                    if GroupID_input=="0":
                        break
                    group_ID_exists=FUNCTIONS.check_group_exists(GroupID_input)
                    if group_ID_exists:
                        print("\nGroup ID already exists! Try again. Enter 0 to go back.\n")
                FUNCTIONS.create_group(GroupID_input, ID_input) #group ID, admin
                if group_ID_exists!="0":
                    print("Group created. You are the admin of this group.")
            elif login_choice=="3":
                group_exists=False
                while not group_exists:
                    print(DASHED_LINE)
                    print("Enter the group ID:")
                    Group_input=input()
                    print(DASHED_LINE)
                    if Group_input=="0":
                        break
                    group_exists=FUNCTIONS.check_group_exists(Group_input)
                    if not group_exists:
                        print("\nGroup ID doesn't exist! Try again. Enter 0 to go back.\n")
                        continue
                    correct_admin=FUNCTIONS.check_admin(Group_input, ID_input)
                    if not correct_admin:
                        group_ID_exists=False
                
                while True:
                    print("\nAs the admin of group "+str(Group_input)+", please choose the action you want to perform:")
                    print(DASHED_LINE)
                    print("0: Exit")
                    print("1: Add member")
                    print("2: Remove member")
                    print(DASHED_LINE)

                    admin_choice=input()

                    if admin_choice!="0" and admin_choice!="1" and admin_choice!="2":
                        print("Invalid choice! Please try again.")
                        continue
                    elif admin_choice=="0":
                        break
                    elif admin_choice=="1":
                        user_id_valid=False
                        while not user_id_valid:
                            print(DASHED_LINE)
                            print("Enter User ID:")
                            user_id_added=input()
                            print(DASHED_LINE)
                            if user_id_added=="0":
                                break
                            user_id_valid=FUNCTIONS.check_user_exists(user_id_added)
                            if not user_id_valid:
                                print("\nUser ID doesn't exist! Try again. Enter 0 to go back.\n")
                        FUNCTIONS.add_member(Group_input, user_id_added)
                        print("User added")
                    elif admin_choice=="2":
                        user_id_valid=False
                        while not user_id_valid:
                            print(DASHED_LINE)
                            print("Enter User ID:")
                            user_id_removed=input()
                            print(DASHED_LINE)
                            if user_id_removed=="0":
                                break
                            user_id_valid=FUNCTIONS.check_user_exists(user_id_removed)
                            if not user_id_valid:
                                print("\nUser ID doesn't exist! Try again. Enter 0 to go back.\n")
                        FUNCTIONS.remove_member(Group_input, user_id_removed)
                        print("User removed")

            elif login_choice=="4":
                group_exists=False
                while not group_exists:
                    print(DASHED_LINE)
                    print("Enter the group ID:")
                    Group_input=input()
                    print(DASHED_LINE)
                    if Group_input=="0":
                        break
                    group_exists=FUNCTIONS.check_group_exists(Group_input)
                    if not group_exists:
                        print("\nGroup ID doesn't exist! Try again. Enter 0 to go back.\n")
                        continue
                    is_user_member=FUNCTIONS.check_member(Group_input, ID_input)
                    if not is_user_member:
                        print("You are not part of this group. Please try again, or enter 0 to go back.")
                        group_ID_exists=False
                
                print(DASHED_LINE)
                print("0: Back")
                print("1: Send a text")
                print("2: Send an image")
                print(DASHED_LINE)
                
                message_choice=input()
                if message_choice not in ["0", "1", "2"]:
                    print("Invalid choice! Please try again.")
                    continue
                elif message_choice=="0":
                    continue
                elif message_choice=="1":
                    print(DASHED_LINE)
                    print("Enter your message:")
                    cur_message=input()
                    print(DASHED_LINE)
                    print("Enter the group ID of the group:")
                    cur_group=input()
                    print(DASHED_LINE)
                    FUNCTIONS.send_group_text(ID_input, cur_group, cur_message)
                    print("Message sent!")
                elif message_choice=="2":
                    print(DASHED_LINE)
                    print("Enter your image directory:")
                    cur_image=input()
                    print(DASHED_LINE)
                    print("Enter the User ID of the receiver:")
                    cur_group=input()
                    print(DASHED_LINE)
                    FUNCTIONS.send_group_image(ID_input, cur_group, cur_image)
                    print("Message sent!")



