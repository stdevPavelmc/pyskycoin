import skycoin
from tests.utils.skyerror import error
from tests.utils import transutil

MaxUint64 = 0xFFFFFFFFFFFFFFFF
Million = 1000000
MaxUint16 = 0xFFFF


def test_TestTransactionVerify():
    # Mismatch header hash
    _, tx = transutil.makeTransaction()
    h = skycoin.cipher_SHA256()
    h.assignTo(tx.InnerHash)
    assert skycoin.SKY_coin_Transaction_Verify(tx) == error["SKY_ERROR"]
    # No inputs
    handle, tx = transutil.makeTransaction()
    assert skycoin.SKY_coin_Transaction_ResetInputs(
        handle, 0) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    # No outputs
    handle, _ = transutil.makeTransaction()
    assert skycoin.SKY_coin_Transaction_ResetOutputs(
        handle, 0) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    # Invalid number of Sigs
    handle, _ = transutil.makeTransaction()
    assert skycoin.SKY_coin_Transaction_ResetSignatures(
        handle, 0) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    assert skycoin.SKY_coin_Transaction_ResetSignatures(
        handle, 20) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    # Too many sigs & inputs
    handle, _ = transutil.makeTransaction()
    assert skycoin.SKY_coin_Transaction_ResetSignatures(
        handle, MaxUint16) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_ResetInputs(
        handle, MaxUint16) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    # Duplicate inputs
    ux, s = transutil.makeUxOutWithSecret()
    handle, _ = transutil.test_makeTransactionFromUxOut(ux, s)
    h = skycoin.cipher_SHA256()
    assert skycoin.SKY_coin_Transaction_Get_Input_At(
        handle, 0, h) == error["SKY_OK"]
    err, _ = skycoin.SKY_coin_Transaction_PushInput(handle, h)
    assert err == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_ResetSignatures(
        handle, 0) == error["SKY_OK"]
    secKeys = []
    secKeys.append(s)
    secKeys.append(s)
    assert skycoin.SKY_coin_Transaction_SignInputs(
        handle, secKeys) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    # Duplicate outputs
    handle, _ = transutil.makeTransaction()
    pOutput = skycoin.coin__TransactionOutput()
    assert skycoin.SKY_coin_Transaction_Get_Output_At(
        handle, 0, pOutput) == error["SKY_OK"]
    pOutput.Address = skycoin.cipher__Address()
    assert skycoin.SKY_coin_Transaction_ResetOutputs(
        handle, 0) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_PushOutput(
        handle, pOutput.Address, pOutput.Coins, pOutput.Hours) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_PushOutput(
        handle, pOutput.Address, pOutput.Coins, pOutput.Hours) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    # Output coins are 0
    handle, _ = transutil.makeTransaction()
    assert skycoin.SKY_coin_Transaction_Get_Output_At(
        handle, 0, pOutput) == error["SKY_OK"]
    pOutput.Coins = 0
    assert skycoin.SKY_coin_Transaction_ResetOutputs(
        handle, 0) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_PushOutput(
        handle, pOutput.Address, pOutput.Coins, pOutput.Hours) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    # Output coin overflow
    handle, _ = transutil.makeTransaction()
    assert skycoin.SKY_coin_Transaction_Get_Output_At(
        handle, 0, pOutput) == error["SKY_OK"]
    pOutput.Coins = int(MaxUint64 - int(3e6))
    assert skycoin.SKY_coin_Transaction_PushOutput(
        handle, pOutput.Address, pOutput.Coins, pOutput.Hours) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_ERROR"]
    # Output coins are not multiples of 1e6 (valid, decimal restriction is not enforced here)
    handle, _ = transutil.makeTransaction()
    assert skycoin.SKY_coin_Transaction_Get_Output_At(
        handle, 0, pOutput) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_ResetOutputs(
        handle, 0) == error["SKY_OK"]
    pOutput.Coins += 10
    assert skycoin.SKY_coin_Transaction_PushOutput(
        handle, pOutput.Address, pOutput.Coins, pOutput.Hours) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_ResetSignatures(handle, 0) == error["SKY_OK"]
    p = skycoin.cipher_PubKey()
    s = skycoin.cipher_SecKey()
    assert skycoin.SKY_cipher_GenerateKeyPair(p, s) == error["SKY_OK"]
    secKeys = []
    secKeys.append(s)
    assert skycoin.SKY_coin_Transaction_SignInputs(handle, secKeys) == error["SKY_OK"]
    assert int(pOutput.Coins % int(1e6)) != int(0)
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_OK"]
    # Valid
    handle, _ = transutil.makeTransaction()
    assert skycoin.SKY_coin_Transaction_Get_Output_At(handle, 0, pOutput) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_ResetOutputs(handle, 0) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_PushOutput(handle, pOutput.Address, int(10e6), pOutput.Hours) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_PushOutput(handle, pOutput.Address, int(1e6), pOutput.Hours) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_UpdateHeader(handle) == error["SKY_OK"]
    assert skycoin.SKY_coin_Transaction_Verify(handle) == error["SKY_OK"]

    
