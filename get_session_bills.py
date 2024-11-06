from legiscanscraper import legiscanscraper
import sys

ls = legiscanscraper()

if __name__ == "__main__":
  ls.get_bill_list(sys.argv[1], make_file=True)