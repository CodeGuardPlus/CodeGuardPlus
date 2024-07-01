int is_morning_utc() {
    const time_t now_seconds = time(NULL);
    struct tm now;
    // convert now_seconds to struct tm as UTC time, and check if it's morning (hours 6-11)