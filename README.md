# Sandwich Chatbot

This app uses an existing `ollama` instance to expose an api endpoint for a chatbot about sandwiches.

You can attach the app using the following command:

```sh
fly launch --attach --from https://github.com/fly-apps/sandwich-chatbot
```

> [!NOTE]  
> You need to run an `ollama` instance and specify the `OLLAMA_HOST` env variable in the `fly.toml`
> You can spin up an instance using `fly launch --from https://github.com/fly-apps/hello-ollama --flycast --name <your-app>`
> Refer to [the repository](https://github.com/fly-apps/hello-ollama) for more information.

## Running the app

First, you will have to specify an `OLLAMA_HOST`.
Make sure your `ollama` has the `llama3.1` model available.
To run the app for local development:

```sh
fastapi dev
```

Once the app is up, you can use the chatbot:
```sh 
curl -X POST "http://localhost:8000/sandwich-chat" \
   -H "Content-Type: application/json" \
   -d '{"session_id": "xyz", "query": "whats a sandwich?"}'
```

```sh
curl -X POST "http://localhost:8000/sandwich-chat" \
   -H "Content-Type: application/json" \
   -d '{"session_id": "xyz", "query": "repeat the last sentence"}'
```