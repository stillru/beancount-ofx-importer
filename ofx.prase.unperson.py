import codecs
import glob
from ofxparse import OfxParser

def ofx_obj(ofx):
    # The OFX object

    ofx.account               # An Account object

    # Account
    account = ofx.account
    account.account_id        # The account number
    account.number            # The account number (deprecated -- returns account_id)
    account.routing_number    # The bank routing number
    account.branch_id         # Transit ID / branch number
    account.type              # An AccountType object
    account.statement         # A Statement object
    account.institution       # An Institution object

    # Statement

    statement = account.statement
    statement.start_date          # The start date of the transactions
    statement.end_date            # The end date of the transactions
    statement.balance             # The money in the account as of the statement date
    #statement.available_balance   # The money available from the account as of the statement date
    statement.transactions        # A list of Transaction objects

    # Transaction

    for transaction in statement.transactions:
        transaction.payee
        transaction.type
        transaction.date
        transaction.amount
        transaction.id
        transaction.memo
        transaction.sic
        transaction.mcc
        transaction.checknum
    return ofx

def select_acc(account):
    global acc
    if account.account_id == 'xxxxx': #Account id
        acc = "Liabilities:RUS:Raiffizen:Mortgage" # Beancount account
    else:
        acc = "NotDefind"
        print("Not my accounts!")
    return acc

def read_file():
    for filename in glob.glob('/*.ofx'): # Directory for ofx files
        with codecs.open(filename) as fileobj:
            ofx = OfxParser.parse(fileobj)
            ofx_obj(ofx)
            select_acc(ofx.account)
            for transaction in reversed(ofx.account.statement.transactions):
                print(transaction.date.strftime("%Y-%m-%d")," ! " + "\"" + transaction.payee + "\"","\n ", acc ,"              {:.2f}".format(transaction.amount), "RUB", "\n  Expenses:Misc\n")

read_file()
