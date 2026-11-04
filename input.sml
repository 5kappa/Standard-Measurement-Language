/*
 * A more involved Standard Measurement Language lexer sample.
 * The current CLI tokenizes this source but does not execute it.
 */
fn speed(distance: Length, elapsed: Time): [m/s] {
    return (distance as m) / (elapsed as s);
}

fn main() {
    const route: [km] = 5km;
    let elapsed: [s] = 18.5s;
    let current_speed = speed(route as m, elapsed);

    print("Calculated speed: ", current_speed);

    if (current_speed > 20[m/s]) then {
        print("The trip is moving quickly.");
    } else {
        print("The trip is within the target speed.");
    }

    for (let sample: int = 0; sample < 3; sample++) do {
        print("Sample number: ", sample);
    }

    assert current_speed > 0[m/s];
}
