from urllib.request import urlopen
import pandas as pd
import time
from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import auto_email
from scoreclass import Scoreclass

# URL of the website to scrape

# url = "http://olympus.realpython.org/profiles/dionysus"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
# }


def read_url(url_in):
    page = urlopen(url_in)
    html = page.read().decode("utf-8")
    # dumbass site doesn't give me truth values correctly
    html = html.replace("true", "True")
    html = html.replace("false", "False")
    dict_out = eval(html)

    return dict_out


def summary(runner):

    # Create summary and plot for viewing
    players = runner.df.Owner.unique()
    win_bin = np.zeros(len(players))
    for i, player in enumerate(players):
        win_bin[i] = runner.df.loc[runner.df.Owner == player, "Wins"].sum()

    csfont = {"fontname": "Comic Sans MS"}
    fig = plt.figure(num=1, dpi=80, edgecolor="k")
    ax = fig.add_subplot(111)
    # ax.set_axis_bgcolor("y")
    plt.bar(players, win_bin, color="c")
    plt.title(f"Standings After Week {runner.week_num}", **csfont)
    plt.grid()
    # plt.show()

    fig.savefig(
        "C:\\Users\\NOTveitB\\Documents\\Python\\Personal\\Scrub Internet\\Standings.png"
    )
    runner.winner = players[int(np.argmax(win_bin))]

    for i, player in enumerate(players):
        runner.send_score_email(runner.email_add[player])

    return runner
    # print(players)


# Send an HTTP GET request to the website
# response = requests.get(url, headers=headers)
if __name__ == "__main__":

    scoreclass = Scoreclass()

    scoreclass.df = pd.read_csv(scoreclass.df_path)

    total_days = date.today() - date(2025, 9, 5)
    iter_num = total_days.days + 1
    # Index through the 7 days of the week(including today)
    # for i in range(iter_num):
    for i in range(40):

        date = date.today() + timedelta(-40 + i)
        # date = date.date(2025, 9, 4)+timedelta(i)
        url = scoreclass.base_url + date.strftime("%Y%m%d")
        html_dict = read_url(url)

        games = html_dict["events"]
        if games == []:
            continue
        week_num = games[0]["week"]["number"]
        s = scoreclass.df.iloc[week_num - 1]
        print(week_num)
        for game in games:
            for team in game["competitions"][0]["competitors"]:
                team_ind = team["team"]["abbreviation"]
                win = team["winner"]
                if win == False:
                    failures = s[s == team_ind].index.tolist()
                    print(f"{team_ind} lost")
                    for failure in failures:
                        scoreclass.df.loc[len(scoreclass.df) - 1, failure] = (
                            int(scoreclass.df.loc[len(scoreclass.df) - 1, failure]) + 1
                        )

        time.sleep(0.25)
    print(scoreclass.df)
    scoreclass.df.to_csv("output.csv", index=False)
    # scoreclass = summary(scoreclass)
    # scoreclass.df.to_csv(scoreclass.df_path, index=False)
