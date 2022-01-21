import json

with open('reddit_jokes.json') as fi:
        fo = open('reddit_jokes_filtered.json', 'w')
        data = json.load(fi)

        count = 0
        goodJokes = []

        for joke in data:
            if joke["score"] >= 100 and len(joke["body"]) < 500 and "\n" not in joke["body"]:
                goodJokes.append(joke)
                count+=1
        
        goodJokesJson = json.dumps(goodJokes, indent=4, sort_keys=True)
        fo.write(goodJokesJson)
        print(count)
