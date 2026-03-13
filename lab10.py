# name: Braedon Stapelman
# date: 3/12/2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5

import boto3
from boto3.dynamodb.conditions import Key, Attr

#constants
REGION = "us-east-1"
TABLE_NAME = "Songs"

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def create_song():
    """Creates a new song"""
    name = input("Enter the name for the new song: ")

    artist = input("Enter the artist for the new song: ")

    table.put_item(
        Item={
            'Name': name,
            'Artist': artist,
            'Ratings': []
        }
    )

    print("creating a song")

def print_song(song):
    """Prints the info for the given song."""
    name = song.get("Name", "Unknown Name")
    artist = song.get("Artist", "Unknown Artist")
    ratings = song.get("Ratings", "No ratings")

    print(f"  Name  : {name}")
    print(f"  Artist: {artist}")
    print(f"  Ratings: {ratings}")
    print()

def print_all_songs():
    """Scan the entire Songs table and print each item."""
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No songs found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} song(s):\n")
    for song in items:
        print_song(song)

def update_rating():
    name = input("What is the song's name? ")
    rating = int(input("What is the rating (integer): "))
    table.update_item(
        Key={"Name": name},
        UpdateExpression="SET Ratings = list_append(Ratings, :r)",
        ExpressionAttributeValues={':r': [rating]}
    )

def delete_song():
    name = input("Enter the name of the song you want to delete: ")
    table.delete_item(
        Key={
            'Name': name
        }
    )
    print("deleting song")

def query_song():
    name = input("Enter the name of the song you want to query: ")
    response = table.get_item(
        Key={
            'Name': name
        }
    )
    item = response.get('Item')
    
    if item and item.get('Ratings'):
        average = round(sum(item['Ratings']) / len(item['Ratings']), 1)
        print(average)
    else:
        print("no ratings found")
    
    print("query song")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (add a review)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_song()
        elif input_char.upper() == "R":
            print_all_songs()
        elif input_char.upper() == "U":
            try:
                update_rating()
            except Exception:
                print("!! error in updating song rating !!")
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            try:
                query_song()
            except Exception:
                print("!! song not found !!")
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()