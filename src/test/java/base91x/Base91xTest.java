/*
MIT License

Copyright (c) 2026 Roman Babenko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
package base91x;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;

/*

TEXT = "The quick brown\r\nfox\tjumps\nover\rthe lazy\n\rdog!"
PANGRAM = "Thequickbrownfoxjumpsoverthelazydog!"
DATA = [88, 136, 162, 112, 31, 156, 195, 75, 208, 5, 61, 106, 20, 163, 227, 172, 240, 150, 163, 100, 63, 170, 82,
        175, 58, 17, 203, 5, 3]
         */

public class Base91xTest {

    public static void main(String[] args) {
        testString();
        testBytes();
        testNull();

        System.out.println("ALL TESTS PASSED");
    }

    private static void testString() {
        byte[] input = "hello".getBytes(StandardCharsets.UTF_8);

        byte[] encoded = Base91x.encode(input);
        byte[] decoded = Base91x.decode(encoded);

        assertArrayEquals(input, decoded, "Refurbish test failed");
    }

    private static void testBytes() {
        byte[] input = new byte[] { 88, (byte) 136, (byte) 162, 112, 31, (byte) 156, (byte) 195, 75, (byte) 208, 5, 61,
                106, 20, (byte) 163, (byte) 227,
                (byte) 172, (byte) 240, (byte) 150, (byte) 163, 100, 63, (byte) 170, 82, (byte) 175, 58, 17, (byte) 203,
                5, 3 };

        byte[] encoded = Base91x.encode(input);
        String actual = new String(encoded, StandardCharsets.US_ASCII);
        assertEquals("Thequickbrownfoxjumpsoverthelazydog!", actual, "Unmatch");
        byte[] decoded = Base91x.decode(encoded);

        assertArrayEquals(input, decoded, "Bytes test failed");
    }

    private static void testNull() {
        assertEquals(null, Base91x.decode((byte[]) null), "Null bytes failed");
    }

    private static void assertEquals(Object expected, Object actual, String message) {
        if (expected == null ? actual != null : !expected.equals(actual)) {
            fail(message + ": expected=" + expected + ", actual=" + actual);
        }
    }

    private static void assertArrayEquals(byte[] expected, byte[] actual, String message) {
        if (!Arrays.equals(expected, actual)) {
            fail(message);
        }
    }

    private static void fail(String message) {
        System.err.println("TEST FAILED: " + message);
        System.exit(1);
    }
}
// rm -fr out && mkdir -p out && javac -d out src/main/java/base91x/Base91x.java src/test/java/base91x/Base91xTest.java && java -cp out base91x.Base91xTest
