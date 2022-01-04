from chkpkg import Package

if __name__ == "__main__":
    with Package() as pkg:
        pkg.run_python_code('from string_trimmer import SuffixTrimmer, PrefixTrimmer, TripleTrimmer')

    print("\nPackage is OK!")

