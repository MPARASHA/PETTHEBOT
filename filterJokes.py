import json

with open('reddit_jokes.json') as fi:
        fo = open('reddit_jokes_filtered.json', 'w')
        data = json.load(fi)

        count = 0
        goodJokes = []

        for joke in data:
            if joke["score"] >= 25:
                goodJokes.append(joke)
                count+=1
        
        goodJokesJson = json.dumps(goodJokes, indent=4, sort_keys=True)
        fo.write(goodJokesJson)
        print(count)
