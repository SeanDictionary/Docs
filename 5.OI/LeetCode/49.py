from typing import *

from collections import Counter

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        tmp = {}
        for s in strs:
            ttmp = str(sorted(Counter(s).items()))
            if ttmp in tmp:
                tmp[ttmp] += [s]
            else:
                tmp[ttmp] = [s]

        return list(tmp.values())


if __name__ == '__main__':
    s = Solution()

    inputs = [
        ["eat", "tea", "tan", "ate", "nat", "bat"]
    ]

    print(s.groupAnagrams(*inputs))
