package utils

import (
	"io/fs"
	"os"
	"path/filepath"
)

// Map applies a given function (fn) to each element of the input slice (ts)
// and returns a new slice containing the results of applying the function.
// The input slice (ts) remains unchanged.
//
// Example usage:
//
//	strings := []string{"apple", "banana", "cherry"}
//	lengths := Map(strings, func(s string) int { return len(s) })
//	// lengths is now []int{5, 6, 6}
func Map[T, V any](ts []T, fn func(T) V) []V {
	result := make([]V, len(ts))
	for i, t := range ts {
		result[i] = fn(t)
	}
	return result
}

// Keys extracts the keys from the given map (M) and returns them as a slice.
//
// Example usage:
//
//	myMap := map[string]int{"one": 1, "two": 2, "three": 3}
//	keys := Keys(myMap)
//	// keys is now []string{"one", "two", "three"}
func Keys[T comparable, V any](M map[T]V) []T {
	result := make([]T, len(M))
	i := 0
	for key := range M {
		result[i] = key
		i++
	}
	return result
}

// GetFiles retrieves a list of file paths that match a specified pattern
// within the given directory and its subdirectories.
//
// Parameters:
//   - path: The root directory to start searching for files.
//   - pattern: The file name pattern to match using filepath.Match.
//
// Returns:
//   - []string: A slice containing paths of files that match the pattern.
//   - error: An error, if any, encountered during the file search.
//
// Example usage:
//
//	files, err := GetFiles("/path/to/directory", "*.txt")
//	if err != nil {
//	    // handle the error
//	}
//	// files now contains the paths of all matching text files.
func GetFiles(path, pattern string) ([]string, error) {
	var paths []string

	err := filepath.Walk(path, func(path string, info fs.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}
		if matched, err := filepath.Match(pattern, filepath.Base(path)); err != nil {
			return err
		} else if matched {
			paths = append(paths, path)
		}
		return nil
	})
	if err != nil {
		return nil, err
	}

	return paths, nil
}

// GetDirectories retrieves a list of directory names within the specified path.
//
// Parameters:
//   - path: The path for which to retrieve directory names.
//
// Returns:
//   - []string: A slice containing names of directories within the specified path.
//   - error: An error, if any, encountered during the directory listing.
//
// Example usage:
//
//	directories, err := GetDirectories("/path/to/parent_directory")
//	if err != nil {
//	    // handle the error
//	}
//	// directories now contains the names of all subdirectories.
func GetDirectories(path string) ([]string, error) {
	var dirs []string

	entries, err := os.ReadDir(path)
	if err != nil {
		return dirs, nil
	}

	for _, e := range entries {
		if e.IsDir() {
			dirs = append(dirs, e.Name())
		}
	}

	return dirs, nil
}
