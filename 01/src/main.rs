use std::option::Option;
use std::io::Stdin;
use std::iter::{Iterator, FromIterator};
use std::vec::Vec;

fn cast_string_to_int(s: &str) -> Option<i64> {
    match s.parse::<i64>() {
        Ok(num) => Some(num),
        Err(_) => None
    }
}

fn trim_end_line_from_string(s: &str) -> String {
    let string_without_end = s.trim_end();
    return String::from(string_without_end)
}

fn read_line_from_stdin(s: &Stdin) -> Option<String> {
    let mut buffer = String::new();
    match s.read_line(&mut buffer) {
        Ok(num_read) => {
            if num_read > 1 {
                return Some(trim_end_line_from_string(&buffer))
            } else {
                return None
            }
        },
        Err(e) => {
            panic!(e);
        }
    }
}

struct FrecuenciasIterator {
    stdin: Stdin
}

impl FrecuenciasIterator {
    pub fn new(stdin: Stdin) -> FrecuenciasIterator {
        FrecuenciasIterator { stdin: stdin }
    }
}

impl Iterator for FrecuenciasIterator {
    type Item = i64;

    fn next(&mut self) -> Option<i64> {
        match read_line_from_stdin(&self.stdin) {
            Some(string) => cast_string_to_int(&string),
            None => None
        }
    }
}

fn main() {
    let fi = FrecuenciasIterator::new(std::io::stdin());
    let deltas = Vec::from_iter(fi);
    let mut found_accumulators_positive = Vec::new();
    let mut found_accumulators_negative = Vec::new();

    let mut accumulator: i64 = 0;
    let mut found_duplicate: bool = false;

    while !found_duplicate {
        for delta in &deltas {
            accumulator += delta;
            if accumulator > 0 {
                if found_accumulators_positive.contains(&accumulator) {
                    println!("Hemos encontrado el acumulador repetido: {}", accumulator);
                    found_duplicate = true;
                    break
                } else {
                    found_accumulators_positive.push(accumulator)
                }
            } else {
                if found_accumulators_negative.contains(&accumulator) {
                    println!("Hemos encontrado el acumulador repetido: {}", accumulator);
                    found_duplicate = true;
                    break
                } else {
                    found_accumulators_negative.push(accumulator)
                }
            }
        }
    }
}
