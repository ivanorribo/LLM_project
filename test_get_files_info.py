
from functions.get_files_info import get_files_info
def test():
    result = get_files_info("calculator", ".")
    print(result)
    result2 = get_files_info("calculator", "pkg")
    print(result2)
    result3 = get_files_info("calculator", "/bin")
    print(result3)
    result4 = get_files_info("calculator", "../")
    print(result4)

if __name__ == "__main__":
    test()