package aezeed

import (
	"bytes"
	"math/rand"
	"testing"
	"testing/quick"
	"time"

	"github.com/stretchr/testify/require"
)

// TestVector defines the values that are used to create a fully initialized
// aezeed mnemonic seed and the expected values that should be calculated.
type TestVector struct {
	version          uint8
	time             time.Time
	entropy          [EntropySize]byte
	salt             [SaltSize]byte
	password         []byte
	expectedMnemonic [NumMnemonicWords]string
	expectedBirthday uint16
}

var (
	testEntropy = [EntropySize]byte{
		0x81, 0xb6, 0x37, 0xd8,
		0x63, 0x59, 0xe6, 0x96,
		0x0d, 0xe7, 0x95, 0xe4,
		0x1e, 0x0b, 0x4c, 0xfd,
	}
	testSalt = [SaltSize]byte{
		0x73, 0x61, 0x6c, 0x74, 0x31, // equal to "salt1"
	}
	version0TestVectors = []TestVector{{
		version:  0,
		time:     BitcoinGenesisDate,
		entropy:  testEntropy,
		salt:     testSalt,
		password: []byte{},
		expectedMnemonic: [NumMnemonicWords]string{
			"ability", "liquid", "travel", "stem", "barely", "drastic",
			"pact", "cupboard", "apple", "thrive", "morning", "oak",
			"feature", "tissue", "couch", "old", "math", "inform",
			"success", "suggest", "drink", "motion", "know", "royal",
		},
		expectedBirthday: 0,
	}, {
		version:  0,
		time:     time.Unix(1521799345, 0), // 03/23/2018 @ 10:02am (UTC)
		entropy:  testEntropy,
		salt:     testSalt,
		password: []byte("!very_safe_55345_password*"),
		expectedMnemonic: [NumMnemonicWords]string{
			"able", "tree", "stool", "crush", "transfer", "cloud",
			"cross", "three", "profit", "outside", "hen", "citizen",
			"plate", "ride", "require", "leg", "siren", "drum",
			"success", "suggest", "drink", "require", "fiscal", "upgrade",
		},
		expectedBirthday: 3365,
	}}
)

func assertCipherSeedEqual(t *testing.T, cipherSeed *CipherSeed,
	cipherSeed2 *CipherSeed) {

	require.Equal(
		t, cipherSeed.InternalVersion, cipherSeed2.InternalVersion,
		"internal version",
	)
	require.Equal(t, cipherSeed.Birthday, cipherSeed2.Birthday, "birthday")
	require.Equal(t, cipherSeed.Entropy, cipherSeed2.Entropy, "entropy")
	require.Equal(t, cipherSeed.salt, cipherSeed2.salt, "salt")
}

// TestAezeedVersion0TestVectors tests some fixed test vector values against
// the expected mnemonic words.
func TestAezeedVersion0TestVectors(t *testing.T) {
	t.Parallel()

	// To minimize the number of tests that need to be run, go through all
	// test vectors in the same test and also check the birthday calculation
	// while we're at it.
	for _, v := range version0TestVectors {
		// First, we create new cipher seed with the given values
		// from the test vector.
		cipherSeed, err := New(v.version, &v.entropy, v.time)
		require.NoError(t, err)

		// Then we need to set the salt to the pre-defined value,
		// otherwise we'll end up with randomness in our mnemonics.
		cipherSeed.salt = v.salt

		// Now that the seed has been created, we'll attempt to convert
		// it to a valid mnemonic.
		mnemonic, err := cipherSeed.ToMnemonic(v.password)
		require.NoError(t, err)

		// Finally we compare the generated mnemonic and birthday to the
		// expected value.
		require.Equal(t, v.expectedMnemonic[:], mnemonic[:])
		require.Equal(t, v.expectedBirthday, cipherSeed.Birthday)
	}
}

// TestWithRandomnessSource tests that seed generation is fully deterministic
// when a custom static randomness source is provided.
func TestWithRandomnessSource(t *testing.T) {
	sourceData := append([]byte{}, testEntropy[:]...)
	sourceData = append(sourceData, testSalt[:]...)
	src := bytes.NewReader(sourceData)

	// First, we create new cipher seed with the given values from the test
	// vector but with no entropy.
	v := version0TestVectors[0]
	cipherSeed, err := New(
		v.version, nil, v.time, WithRandomnessSource(src),
	)
	require.NoError(t, err)

	// The salt should be set to our test salt.
	require.Equal(t, testSalt, cipherSeed.salt)

	// Now that the seed has been created, we'll attempt to convert it to a
	// valid mnemonic.
	mnemonic, err := cipherSeed.ToMnemonic(v.password)
	require.NoError(t, err)

	// Finally, we compare the generated mnemonic and birthday to the
	// expected value.
	require.Equal(t, v.expectedMnemonic[:], mnemonic[:])
	require.Equal(t, v.expectedBirthday, cipherSeed.Birthday)
}

// TestEmptyPassphraseDerivation tests that the aezeed scheme is able to derive
// a proper mnemonic, and decipher that mnemonic when the user uses an empty
// passphrase.
func TestEmptyPassphraseDerivation(t *testing.T) {
	t.Parallel()

	// Our empty passphrase...
	pass := []byte{}

	// We'll now create a new cipher seed with an internal version of zero
	// to simulate a wallet that just adopted the scheme.
	cipherSeed, err := New(0, &testEntropy, time.Now())
	require.NoError(t, err)

	// Now that the seed has been created, we'll attempt to convert it to a
	// valid mnemonic.
	mnemonic, err := cipherSeed.ToMnemonic(pass)
	require.NoError(t, err)

	// Next, we'll try to decrypt the mnemonic with the passphrase that we
	// used.
	cipherSeed2, err := mnemonic.ToCipherSeed(pass)
	require.NoError(t, err)

	// Finally, we'll ensure that the uncovered cipher seed matches
	// precisely.
	assertCipherSeedEqual(t, cipherSeed, cipherSeed2)
}

// TestManualEntropyGeneration tests that if the user doesn't provide a source
// of entropy, then we do so ourselves.
func TestManualEntropyGeneration(t *testing.T) {
	t.Parallel()

	// Our empty passphrase...
	pass := []byte{}

	// We'll now create a new cipher seed with an internal version of zero
	// to simulate a wallet that just adopted the scheme.
	cipherSeed, err := New(0, nil, time.Now())
	require.NoError(t, err)

	// Now that the seed has been created, we'll attempt to convert it to a
	// valid mnemonic.
	mnemonic, err := cipherSeed.ToMnemonic(pass)
	require.NoError(t, err)

	// Next, we'll try to decrypt the mnemonic with the passphrase that we
	// used.
	cipherSeed2, err := mnemonic.ToCipherSeed(pass)
	require.NoError(t, err)

	// Finally, we'll ensure that the uncovered cipher seed matches
	// precisely.
	assertCipherSeedEqual(t, cipherSeed, cipherSeed2)
}

// TestInvalidPassphraseRejection tests if a caller attempts to use the
// incorrect passphrase for an enciphered seed, then the proper error is
// returned.
func TestInvalidPassphraseRejection(t *testing.T) {
	t.Parallel()

	// First, we'll generate a new cipher seed with a test passphrase.
	pass := []byte("test")
	cipherSeed, err := New(0, &testEntropy, time.Now())
	require.NoError(t, err)

	// Now that we have our cipher seed, we'll encipher it and request a
	// mnemonic that we can use to recover later.
	mnemonic, err := cipherSeed.ToMnemonic(pass)
	require.NoError(t, err)

	// If we try to decipher with the wrong passphrase, we should get the
	// proper error.
	wrongPass := []byte("kek")
	_, err = mnemonic.ToCipherSeed(wrongPass)
	require.Equal(t, ErrInvalidPass, err)
}

// TestRawEncipherDecipher tests that callers are able to use the raw methods
// to map between ciphertext and the raw plaintext deciphered seed.
func TestRawEncipherDecipher(t *testing.T) {
	t.Parallel()

	// First, we'll generate a new cipher seed with a test passphrase.
	pass := []byte("test")
	cipherSeed, err := New(0, &testEntropy, time.Now())
	require.NoError(t, err)

	// With the cipher seed obtained, we'll now use the raw encipher method
	// to obtain our final cipher text.
	cipherText, err := cipherSeed.Encipher(pass)
	require.NoError(t, err)

	mnemonic, err := cipherTextToMnemonic(cipherText)
	require.NoError(t, err)

	// Now that we have the ciphertext (mapped to the mnemonic), we'll
	// attempt to decipher it raw using the user's passphrase.
	plainSeedBytes, salt, err := mnemonic.Decipher(pass)
	require.NoError(t, err)
	require.Equal(t, cipherSeed.salt, salt)

	// If we deserialize the plaintext seed bytes, it should exactly match
	// the original cipher seed.
	newSeed := CipherSeed{
		salt: salt,
	}
	err = newSeed.decode(bytes.NewReader(plainSeedBytes[:]))
	require.NoError(t, err)

	assertCipherSeedEqual(t, cipherSeed, &newSeed)
}

// TestInvalidExternalVersion tests that if we present a ciphertext with the
// incorrect version to decipherCipherSeed, then it fails with the expected
// error.
func TestInvalidExternalVersion(t *testing.T) {
	t.Parallel()

	// First, we'll generate a new cipher seed.
	cipherSeed, err := New(0, &testEntropy, time.Now())
	require.NoError(t, err)

	// With the cipher seed obtained, we'll now use the raw encipher method
	// to obtain our final cipher text.
	pass := []byte("newpasswhodis")
	cipherText, err := cipherSeed.Encipher(pass)
	require.NoError(t, err)

	// Now that we have the cipher text, we'll modify the first byte to be
	// an invalid version.
	cipherText[0] = 44

	// With the version swapped, if we try to decipher it, (no matter the
	// passphrase), it should fail.
	_, _, err = decipherCipherSeed(cipherText, []byte("kek"))
	require.Equal(t, ErrIncorrectVersion, err)
}

// TestChangePassphrase tests that we're able to generate a cipher seed, then
// change the password. If we attempt to decipher the new enciphered seed, then
// we should get the exact same seed back.
func TestChangePassphrase(t *testing.T) {
	t.Parallel()

	// First, we'll generate a new cipher seed with a test passphrase.
	pass := []byte("test")
	cipherSeed, err := New(0, &testEntropy, time.Now())
	require.NoError(t, err)

	// Now that we have our cipher seed, we'll encipher it and request a
	// mnemonic that we can use to recover later.
	mnemonic, err := cipherSeed.ToMnemonic(pass)
	require.NoError(t, err)

	// Now that have the mnemonic, we'll attempt to re-encipher the
	// passphrase in order to get a brand-new mnemonic.
	newPass := []byte("strongerpassyeh!")
	newMnemonic, err := mnemonic.ChangePass(pass, newPass)
	require.NoError(t, err)

	// We'll now attempt to decipher the new mnemonic using the new
	// passphrase to arrive at (what should be) the original cipher seed.
	newCipherSeed, err := newMnemonic.ToCipherSeed(newPass)
	require.NoError(t, err)

	// Now that we have the cipher seed, we'll verify that the plaintext
	// seed matches *identically*.
	assertCipherSeedEqual(t, cipherSeed, newCipherSeed)
}

// TestChangePassphraseWrongPass tests that if we have a valid enciphered
// cipher seed, but then try to change the password with the *wrong* password,
// then we get an error.
func TestChangePassphraseWrongPass(t *testing.T) {
	t.Parallel()

	// First, we'll generate a new cipher seed with a test passphrase.
	pass := []byte("test")
	cipherSeed, err := New(0, &testEntropy, time.Now())
	require.NoError(t, err)

	// Now that we have our cipher seed, we'll encipher it and request a
	// mnemonic that we can use to recover later.
	mnemonic, err := cipherSeed.ToMnemonic(pass)
	require.NoError(t, err)

	// Now that have the mnemonic, we'll attempt to re-encipher the
	// passphrase in order to get a brand-new mnemonic. However, we'll be
	// using the *wrong* passphrase. This should result in an
	// ErrInvalidPass error.
	wrongPass := []byte("kek")
	newPass := []byte("strongerpassyeh!")
	_, err = mnemonic.ChangePass(wrongPass, newPass)
	require.Equal(t, ErrInvalidPass, err)
}

// TestMnemonicEncoding uses quickcheck like property based testing to ensure
// that we're always able to fully recover the original byte stream encoded
// into the mnemonic phrase.
func TestMnemonicEncoding(t *testing.T) {
	t.Parallel()

	// mainScenario is the main driver of our property based test. We'll
	// ensure that given a random byte string of length 33 bytes, if we
	// convert that to the mnemonic, then we should be able to reverse the
	// conversion.
	mainScenario := func(cipherSeedBytes [EncipheredCipherSeedSize]byte) bool {
		mnemonic, err := cipherTextToMnemonic(cipherSeedBytes)
		if err != nil {
			t.Fatalf("unable to map cipher text: %v", err)
			return false
		}

		newCipher := mnemonicToCipherText(&mnemonic)

		if newCipher != cipherSeedBytes {
			t.Fatalf("cipherseed doesn't match: expected %v, got %v",
				cipherSeedBytes, newCipher)
			return false
		}

		return true
	}

	if err := quick.Check(mainScenario, nil); err != nil {
		t.Fatalf("fuzz check failed: %v", err)
	}
}

// TestEncipherDecipher is a property-based test that ensures that given a
// version, entropy, and birthday, then we're able to map that to a cipher seed
// mnemonic, then back to the original plaintext cipher seed.
func TestEncipherDecipher(t *testing.T) {
	t.Parallel()

	// mainScenario is the main driver of our property based test. We'll
	// ensure that given a random seed tuple (internal version, entropy,
	// and birthday) we're able to convert that to a valid cipher seed.
	// Additionally, we should be able to decipher the final mnemonic, and
	// recover the original cipher seed.
	mainScenario := func(version uint8, entropy [EntropySize]byte,
		nowInt int64, pass [20]byte) bool {

		now := time.Unix(nowInt, 0)

		cipherSeed, err := New(version, &entropy, now)
		if err != nil {
			t.Fatalf("unable to map cipher text: %v", err)
			return false
		}

		mnemonic, err := cipherSeed.ToMnemonic(pass[:])
		if err != nil {
			t.Fatalf("unable to generate mnemonic: %v", err)
			return false
		}

		cipherSeed2, err := mnemonic.ToCipherSeed(pass[:])
		if err != nil {
			t.Fatalf("unable to decrypt cipher seed: %v", err)
			return false
		}

		if cipherSeed.InternalVersion != cipherSeed2.InternalVersion {
			t.Fatalf("mismatched versions: expected %v, got %v",
				cipherSeed.InternalVersion, cipherSeed2.InternalVersion)
			return false
		}
		if cipherSeed.Birthday != cipherSeed2.Birthday {
			t.Fatalf("mismatched birthday: expected %v, got %v",
				cipherSeed.Birthday, cipherSeed2.Birthday)
			return false
		}
		if cipherSeed.Entropy != cipherSeed2.Entropy {
			t.Fatalf("mismatched versions: expected %x, got %x",
				cipherSeed.Entropy[:], cipherSeed2.Entropy[:])
			return false
		}

		return true
	}

	if err := quick.Check(mainScenario, nil); err != nil {
		t.Fatalf("fuzz check failed: %v", err)
	}
}

// TestSeedEncodeDecode tests that we're able to reverse the encoding of an
// arbitrary raw seed.
func TestSeedEncodeDecode(t *testing.T) {
	// mainScenario is the primary driver of our property-based test. We'll
	// ensure that given a random cipher seed, we can encode it and decode
	// it precisely.
	mainScenario := func(version uint8, nowInt int64,
		entropy [EntropySize]byte) bool {

		now := time.Unix(nowInt, 0)
		day := time.Hour * 24
		numDaysSinceGenesis := now.Sub(BitcoinGenesisDate) / day
		seed := CipherSeed{
			InternalVersion: version,
			Birthday:        uint16(numDaysSinceGenesis),
			Entropy:         entropy,
		}

		var b bytes.Buffer
		if err := seed.encode(&b); err != nil {
			t.Fatalf("unable to encode: %v", err)
			return false
		}

		var newSeed CipherSeed
		if err := newSeed.decode(&b); err != nil {
			t.Fatalf("unable to decode: %v", err)
			return false
		}

		if seed.InternalVersion != newSeed.InternalVersion {
			t.Fatalf("mismatched versions: expected %v, got %v",
				seed.InternalVersion, newSeed.InternalVersion)
			return false
		}
		if seed.Birthday != newSeed.Birthday {
			t.Fatalf("mismatched birthday: expected %v, got %v",
				seed.Birthday, newSeed.Birthday)
			return false
		}
		if seed.Entropy != newSeed.Entropy {
			t.Fatalf("mismatched versions: expected %x, got %x",
				seed.Entropy[:], newSeed.Entropy[:])
			return false
		}

		return true
	}

	if err := quick.Check(mainScenario, nil); err != nil {
		t.Fatalf("fuzz check failed: %v", err)
	}
}

// TestDecipherUnknownMnemonicWord tests that if we obtain a mnemonic, then
// modify one of the words to not be within the word list, then it's detected
// when we attempt to map it back to the original cipher seed.
func TestDecipherUnknownMnemonicWord(t *testing.T) {
	t.Parallel()

	// First, we'll create a new cipher seed with "test" ass a password.
	pass := []byte("test")
	cipherSeed, err := New(0, &testEntropy, time.Now())
	require.NoError(t, err)

	// Now that we have our cipher seed, we'll encipher it and request a
	// mnemonic that we can use to recover later.
	mnemonic, err := cipherSeed.ToMnemonic(pass)
	require.NoError(t, err)

	// Before we attempt to decrypt the cipher seed, we'll mutate one of
	// the word so it isn't actually in our final word list.
	randIndex := rand.Int31n(int32(len(mnemonic)))
	mnemonic[randIndex] = "kek"

	// If we attempt to map back to the original cipher seed now, then we
	// should get ErrUnknownMnemonicWord.
	_, err = mnemonic.ToCipherSeed(pass)
	wordErr := &ErrUnknownMnemonicWord{}
	require.ErrorAs(t, err, wordErr)
	require.Equal(t, "kek", wordErr.Word)
	require.Equal(t, uint8(randIndex), wordErr.Index)

	// If the mnemonic includes a word that is not in the englishList it
	// fails, even when it is a substring of a valid word Example: `heart`
	// is in the list, `hear` is not.
	mnemonic[randIndex] = "hear"

	// If we attempt to map back to the original cipher seed now, then we
	// should get ErrUnknownMnemonicWord.
	_, err = mnemonic.ToCipherSeed(pass)
	require.ErrorAs(t, err, wordErr)
}

// TestDecipherIncorrectMnemonic tests that if we obtain a cipher seed, but then
// swap out words, then checksum fails.
func TestDecipherIncorrectMnemonic(t *testing.T) {
	// First, we'll create a new cipher seed with "test" ass a password.
	pass := []byte("test")
	cipherSeed, err := New(0, &testEntropy, time.Now())
	require.NoError(t, err)

	// Now that we have our cipher seed, we'll encipher it and request a
	// mnemonic that we can use to recover later.
	mnemonic, err := cipherSeed.ToMnemonic(pass)
	require.NoError(t, err)

	// We'll now swap out two words from the mnemonic, which should trigger
	// a checksum failure.
	swapIndex1 := 9
	swapIndex2 := 13
	mnemonic[swapIndex1], mnemonic[swapIndex2] = mnemonic[swapIndex2], mnemonic[swapIndex1]

	// If we attempt to decrypt now, we should get a checksum failure.
	// If we attempt to map back to the original cipher seed now, then we
	// should get ErrIncorrectMnemonic.
	_, err = mnemonic.ToCipherSeed(pass)
	require.Equal(t, ErrIncorrectMnemonic, err)
}

// TODO(roasbeef): add test failure checksum fail is modified, new error

func init() {
	// For the purposes of our test, we'll crank down the scrypt params a
	// bit.
	scryptN = 16
	scryptR = 8
	scryptP = 1
}
