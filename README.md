
**Quick Setup**


Install python virtual environment onto your sytem first.

Install pip

Create a virtual env directory under venv/ in the project root.

Run `python -m venv venv`

Run `source venv/bin/activate`


Run `pip install`

If all is well, you're now almost ready.

Run `cp .env.example .env` and update the contents of `.env` with your credentials.

To start with you can try out things like

`python app.py --action=buy --strategy=gold300 --to_club=0` which will try to buy some items using on of the buy strategies, in this case gold300.
Make sure that you're logged out of console and not interacting the web app or companion app.

Enjoy!!!





