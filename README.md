For now, the backend and frontend both have their own serving stack and are run on different ports. This will be fixed in the future.... presumably.

The backend is built with Flask. Run it with:
```
export FLASK_DEBUG=1
flask run
```

The frontend is built with React. Run it with
```
yarn start run
```
