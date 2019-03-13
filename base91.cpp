#include <cstring>
#include <iostream>
#include <fstream>

#include "base91.h"

//------------------------------------------------------------------------------

template<typename Container>
void
readFile(const std::string & fileName, Container &container)
{
	std::fstream fs(fileName, std::ios::in | std::ios::binary);
	if (fs.is_open() and fs.good())
	{
		fs.seekg(0, std::ios::end);
		auto newSize = fs.tellp();
		fs.seekg(0, std::ios::beg);
		container.clear();
		container.resize(newSize);
		fs.read(&container[0], newSize);
		fs.close();
	}
	return;
}

//------------------------------------------------------------------------------

template<typename Container>
void
writeFile(const std::string & fileName, const Container &container)
{
	std::fstream fs(fileName, std::ios::trunc | std::ios::out | std::ios::binary);

	if (fs.good())
	{
		fs.write(container.data(), container.size());
		fs.close();
	}
	return;
}

//------------------------------------------------------------------------------

int
main(const int argc, const char *argv[])
{
	if (argc!=4 or not(0==strncmp("-e", argv[1], 3) or 0==strncmp("-d", argv[1], 3)))
	{
		std::cerr << "base91 -e|-d <in-file> <out-file>";
		return -1;
	}

	if (0==strncmp("-e", argv[1], 3))
	{
		std::vector<char> in;
		std::string out;

		readFile(argv[2], in);
		base91::encode(in, out);
		writeFile(argv[3], out);
	}
	else
	{
		std::string in;
		std::vector<char> out;

		readFile(argv[2], in);
		base91::decode(in, out);
		writeFile(argv[3], out);
	}

	return 0;
}

//------------------------------------------------------------------------------

