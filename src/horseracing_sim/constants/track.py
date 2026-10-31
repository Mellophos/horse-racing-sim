from enum import IntEnum, unique


@unique
class TrackID(IntEnum):
    # Japan
    #   100xx JRA
    SAPPORO = 10001
    HAKODATE = 10002
    NIIGATA = 10003
    FUKUSHIMA = 10004
    NAKAYAMA = 10005
    TOKYO = 10006
    CHUKYO = 10007
    KYOTO = 10008
    HANSHIN = 10009
    KOKURA = 10010

    #   101xx NAR
    MOMBETSU = 10101
    MORIOKA = 10102
    MIZUSAWA = 10103
    URAWA = 10104
    FUNABASHI = 10105
    OI = 10106
    KAWASAKI = 10107
    KANAZAWA = 10108
    NAGOYA = 10109
    KASAMATSU = 10110
    SONODA = 10111
    HIMEJI = 10112
    KOCHI = 10113
    SAGA = 10114

    # Americas
    # 20xxx
    #   200xx USA
    #   201xx Canada
    #   202xx Mexico
    #   203xx South America

    # Asia
    # 30xxx
    #   300xx Hong Kong / China
    #   301xx South Korea
    #   302xx Southeast Asia
    #   303xx South Asia

    # EU / Continental Europe
    # 40xxx
    #   400xx France
    #   401xx Germany
    #   402xx Italy
    #   403xx Spain
    #   404xx Scandinavia
    #   405xx Others

    # UK / Ireland
    # 50xxx
    #   500xx UK
    #   501xx Ireland

    # Oceania
    # 60xxx
    #   600xx Australia
    #   601xx New Zealand

    # Africa
    # 70xxx
    #   700xx South Africa
    #   701xx Others

    # Middle East
    # 80xxx
    #   800xx UAE
    #   801xx Saudi Arabia
    #   802xx Others

    # 90xxx Reserved

    def capitalize(self):
        return self.name.capitalize()
