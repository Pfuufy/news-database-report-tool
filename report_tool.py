#!/usr/bin/python2

import psycopg2


def connect():
    """This function connects to the database and returns the database
    object and its cursor."""

    db = psycopg2.connect(database="news")
    c = db.cursor()
    return db, c


def print_pretty(list_of_touples, measure):
    """This function takes as input a list of two item touples and measure
    The measure is the unit of measurement for the touple items.

    example:
            touple = article, 500
            measure = 'total views'
    prints: 'article - 500 total views' """

    for item in list_of_touples:
        print "%s - %s%s" % (item[0], item[1], measure)
    return


def print_line():
    """This funciton prints a long line and new line to help format results."""

    print "\n--------------------------------------\n"
    return


def get_three_most_pop_articles():
    """This function returns the three most popular articles and their
    total view count."""

    db, c = connect()

    c.execute("""
        select articles.title, article_views.num
        from articles join article_views
        on articles.slug = article_views.slug
        order by article_views.num desc
        limit 3;""")
    article_popularity = c.fetchall()
    db.close()
    return article_popularity


def get_most_popular_authors():
    """This function returns the article authors in descending popularity
    and their total view count."""

    db, c = connect()

    c.execute("""
        select authors.name, sum(article_views.num)
        from articles join article_views
        on articles.slug = article_views.slug
        join authors on authors.id = articles.author
        group by authors.name
        order by sum(article_views.num) desc;
        """)
    artist_popularity = c.fetchall()
    db.close()
    return artist_popularity


def get_request_errors():
    """This function returns the days in which HTTP request errors are
    greater than or equal to 1% of all requests and their corresponding
    percentage of errors."""

    db, c = connect()

    c.execute("""
        select total_requests.time::date,
        round((cast(request_errors.errors as numeric) /
        cast(total_requests.requests as numeric) * 100), 2)
        from total_requests join request_errors
        on total_requests.time::date = request_errors.time::date
        where cast(request_errors.errors as numeric) /
        cast(total_requests.requests as numeric) > .01;
        """)
    request_errors = c.fetchall()
    db.close()
    return request_errors


def print_three_most_pop_articles():
    """This function returns the output of print_pretty with the
    input of the get_three_most_popular_articles function and the
    measure 'total views'."""

    return print_pretty(get_three_most_pop_articles(), " total views")


def print_most_popular_authors():
    """This function returns the output of print_pretty with the
    input of the get_most_popular_authors function and the measure
    'total views'."""

    return print_pretty(get_most_popular_authors(), " total views")


def print_request_errors():
    """This funciton returns the output of print_pretty with the
    input of the get_request_errors function and the measure
    '% errors'."""

    return print_pretty(get_request_errors(), "% errors")


def run():
    """This function ties together all other functions."""

    print "\nThree most popular articles:\n"
    print_three_most_pop_articles()
    print_line()
    print "Most popular authors:\n"
    print_most_popular_authors()
    print_line()
    print "Request errors > 1%:\n"
    print_request_errors()
    print "\nDone\n"


if __name__ == "__main__":
    run()
