package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"slices"
	"strings"
)

// TRR is a struct containing relevant metadata for index.json.
type TRR struct {
	Contributors []string          `json:"contributors"`
	ExternalIDs  []string          `json:"external_ids"`
	ID           string            `json:"id"`
	Keywords     []string          `json:"keywords,omitempty"`
	Name         string            `json:"name"`
	Platforms    []string          `json:"platforms"`
	Procedures   map[string]string `json:"procedures"`
	PubDate      string            `json:"pub_date"`
	Tactics      []string          `json:"tactics"`
}

func (trr *TRR) init() *TRR {
	if trr.ExternalIDs == nil {
		trr.ExternalIDs = []string{}
	}

	return trr
}

var trrRegex *regexp.Regexp = regexp.MustCompile(
	`^(reports/trr\d+)/([^/]+)/metadata.json$`,
)

func caseInsensitive(a string, b string) int {
	var l string = strings.ToLower(a)
	var r string = strings.ToLower(b)

	if l < r {
		return -1
	} else if l > r {
		return 1
	}

	return 0
}

func exit(e error) {
	if e != nil {
		fmt.Printf("[!] %s\n", e)
	}

	os.Exit(1)
}

func main() {
	var buf *bytes.Buffer
	var e error
	var enc *json.Encoder
	var root string = "reports"
	var trrs []TRR = []TRR{}

	// Find all completed TRRs
	fmt.Printf("[*] Gathering TRRs\n")
	e = filepath.WalkDir(
		root,
		func(path string, _ fs.DirEntry, e error) error {
			var b []byte
			var m []string
			var md string
			var trr TRR

			if e != nil {
				return e
			}

			// OS-agnostic
			path = strings.TrimPrefix(filepath.ToSlash(path), "./")

			// Looking for TRRs
			if m = trrRegex.FindStringSubmatch(path); len(m) == 0 {
				return nil
			}

			// Read in metadata.json
			if b, e = os.ReadFile(path); e != nil {
				return e
			}

			// Convert to TRR
			if e = json.Unmarshal(b, &trr); e != nil {
				return e
			}

			trrs = append(trrs, *trr.init())

			// Generate list of unique keywords for filtering
			md = filepath.ToSlash(filepath.Dir(path) + "/README.md")
			trr.Keywords, e = uniqKeywordsMaxLength(md, 1)
			if e != nil {
				return e
			}

			return nil
		},
	)
	if e != nil {
		exit(e)
	}

	slices.SortFunc(trrs, sortTRRs)

	fmt.Printf("[*] Generating index.json\n")
	buf = bytes.NewBuffer([]byte{})
	enc = json.NewEncoder(buf)
	enc.SetEscapeHTML(false)
	enc.SetIndent("", "  ")
	if e = enc.Encode(trrs); e != nil {
		exit(e)
	}

	if e = os.WriteFile("index.json", buf.Bytes(), 0o600); e != nil {
		exit(e)
	}
}

func normalize(s string) string {
	s = strings.Trim(s, "!@#%^&*,-_`:;\"'|")
	return strings.TrimRight(s, "!@#%^&*,.-_`:;\"'/|")
}

func sortTRRs(a TRR, b TRR) int {
	var l string = strings.ToLower(a.ID)
	var lp []string
	var r string = strings.ToLower(b.ID)
	var rp []string

	if l == r {
		lp = append(lp, a.Platforms...)
		slices.SortFunc(lp, caseInsensitive)

		rp = append(rp, b.Platforms...)
		slices.SortFunc(rp, caseInsensitive)

		l = strings.ToLower(a.Platforms[0])
		r = strings.ToLower(b.Platforms[0])
	}

	if l < r {
		return -1
	} else if l > r {
		return 1
	}

	return 0
}

func uniqKeywordsMaxLength(fn string, max int) ([]string, error) {
	var b []byte
	var e error
	var keywords []string
	var s string
	var uniq map[string]struct{} = map[string]struct{}{}

	if fn == "" {
		return nil, nil
	}

	if b, e = os.ReadFile(fn); e != nil {
		return nil, e
	}

	s = strings.ReplaceAll(string(b), "[", " ")
	s = strings.ReplaceAll(s, "]", " ")
	s = strings.ReplaceAll(s, "(", " ")
	s = strings.ReplaceAll(s, ")", " ")
	s = strings.ReplaceAll(s, ",", " ")

	for _, w := range strings.Fields(s) {
		w = normalize(w)

		if (max > 0) && (len(w) > max) {
			continue
		}

		switch len(w) {
		case 0, 1:
			continue
		case 2:
			switch w {
			case "AD":
			default:
				continue
			}
		}

		uniq[strings.ToLower(w)] = struct{}{}
	}

	for w := range uniq {
		keywords = append(keywords, w)
	}

	slices.Sort(keywords)

	return keywords, nil
}
