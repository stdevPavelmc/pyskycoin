import skycoin
from tests.utils.skyerror import error

MaxUint64 = 0xFFFFFFFFFFFFFFFF
Million = 1000000
MaxUint16 = 0xFFFF


def makeAddress():
    p = skycoin.cipher_PubKey()
    s = skycoin.cipher_SecKey()
    assert skycoin.SKY_cipher_GenerateKeyPair(p, s) == error["SKY_OK"]
    a = skycoin.cipher__Address()
    assert skycoin.SKY_cipher_AddressFromPubKey(p, a) == error["SKY_OK"]
    return a


def makeTransactionFromUxOut(ux, s):
    _, handle = skycoin.SKY_coin_Create_Transaction()
    _, tx = skycoin.SKY_coin_Get_Transaction_Object(handle)
    h = skycoin.cipher_SHA256()
    assert skycoin.SKY_cipher_SecKey_Verify(s) == error["SKY_OK"]
    assert skycoin.SKY_coin_UxOut_Hash(ux, h) == error["SKY_OK"]
    err, r = skycoin.SKY_coin_Transaction_PushInput(handle, h)
    assert err == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_PushOutput(
        handle, makeAddress(), int(1e6), int(50)) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_PushOutput(
        handle, makeAddress(), int(5e6), int(50)) == error["SKY_OK"]
    secKeys = []
    secKeys.append(s)
    assert skycoin.SKY_coin_Transaction_SignInputs(
        handle, secKeys) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    return handle, tx


def makeUxBodyWithSecret():
    p = skycoin.cipher_PubKey()
    s = skycoin.cipher_SecKey()
    assert skycoin.SKY_cipher_GenerateKeyPair(p, s) == error["SKY_OK"]
    uxb = skycoin.coin__UxBody()
    err, b = skycoin.SKY_cipher_RandByte(128)
    assert err == error["SKY_OK"]
    h = skycoin.cipher_SHA256()
    assert skycoin.SKY_cipher_SumSHA256(b, h) == error["SKY_OK"]
    assert h.assignTo(uxb.SrcTransaction) == None
    a = skycoin.cipher__Address()
    assert skycoin.SKY_cipher_AddressFromPubKey(p, a) == error["SKY_OK"]
    uxb.Address = a
    uxb.Coins = int(1e6)
    uxb.Hours = int(100)
    return uxb, s


def makeUxOutWithSecret():
    body, sec = makeUxBodyWithSecret()
    uxo = skycoin.coin__UxOut()
    uxh = skycoin.coin__UxHead()
    uxh.Time = 100
    uxh.BkSeq = 2
    uxo.Head = uxh
    uxo.Body = body
    return uxo, sec


def makeTransaction():
    ux, s = makeUxOutWithSecret()
    return makeTransactionFromUxOut(ux, s)


def makeTransactions(n):
    _, handle = skycoin.SKY_coin_Create_Transactions()
    for i in range(n):
        thandle, _ = makeTransaction()
        assert skycoin.SKY_coin_Transactions_Add(
            handle, thandle) == error["SKY_OK"]
    return handle


def copyTransaction(handle):
    handle2 = skycoin.coin__Transaction()
    err, handle2 = skycoin.SKY_coin_Transaction_Copy(
        handle)
    assert err == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle2) == error["SKY_OK"]
    err, ptx = skycoin.SKY_coin_Get_Transaction_Object(handle2)
    assert err == error["SKY_OK"]
    return handle2, ptx


def makeEmptyTransaction():
    _, handle = skycoin.SKY_coin_Create_Transaction()
    return handle


def makeUxOut():
    pOut, _ = makeUxOutWithSecret()
    return pOut


def equalTransactions(handle1, handle2):
    err, size1 = skycoin.SKY_coin_Transactions_Length(handle1)
    assert err == error["SKY_OK"]
    err, size2 = skycoin.SKY_coin_Transactions_Length(handle2)
    assert err == error["SKY_OK"]
    if size1 != size2:
        return 1

    for i in range(int(size1 - 1)):
        err, tx1 = skycoin.SKY_coin_Transactions_GetAt(handle1, i)
        assert err == error["SKY_OK"]
        err, tx2 = skycoin.SKY_coin_Transactions_GetAt(handle2, i)
        assert err == error["SKY_OK"]
        err, tx1_obj = skycoin.SKY_coin_Get_Transaction_Object(tx1)
        assert err == error["SKY_OK"]
        err, tx2_obj = skycoin.SKY_coin_Get_Transaction_Object(tx2)
        assert err == error["SKY_OK"]
        assert tx1_obj == tx2_obj
        i += 1

    return 0