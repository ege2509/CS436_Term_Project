const mysql = require('mysql2/promise');

exports.bookingReport = async (req, res) => {
  let connection;

  try {
    connection = await mysql.createConnection({
      host: '34.116.211.138',
      user: 'appuser',
      password: 'E1m1c1kege.',
      database: 'movie_booking_db',
      port: 3306
    });

    // Main summary
    const [summary] = await connection.execute(`
      SELECT 
        m.title AS movie_title,
        COUNT(DISTINCT b.id) AS total_bookings,
        COUNT(bs.id) AS total_seats_booked,
        COUNT(DISTINCT b.user_id) AS unique_users,
        ROUND(COUNT(bs.id) / COUNT(DISTINCT b.id), 2) AS avg_seats_per_booking
      FROM movies m
      LEFT JOIN bookings b ON m.id = b.movie_id
      LEFT JOIN booking_seats bs ON b.id = bs.booking_id
      GROUP BY m.id
      ORDER BY total_bookings DESC;
    `);

    // Booking distribution by time of day
    const [timeslotStats] = await connection.execute(`
      SELECT 
        CASE 
          WHEN HOUR(booking_time) BETWEEN 6 AND 11 THEN 'Morning'
          WHEN HOUR(booking_time) BETWEEN 12 AND 17 THEN 'Afternoon'
          WHEN HOUR(booking_time) BETWEEN 18 AND 21 THEN 'Evening'
          ELSE 'Night'
        END AS timeslot,
        COUNT(*) AS bookings
      FROM bookings
      GROUP BY timeslot
      ORDER BY FIELD(timeslot, 'Morning', 'Afternoon', 'Evening', 'Night');
    `);

    // Most booked day
    const [topDay] = await connection.execute(`
      SELECT 
        DATE(booking_time) AS booking_date,
        COUNT(*) AS total_bookings
      FROM bookings
      GROUP BY booking_date
      ORDER BY total_bookings DESC
      LIMIT 1;
    `);

    // Daily breakdown for charting
    const [dailyStats] = await connection.execute(`
      SELECT 
        DATE(booking_time) AS day,
        COUNT(*) AS total_bookings
      FROM bookings
      GROUP BY day
      ORDER BY day;
    `);

    res.status(200).json({
      summary,
      timeslotStats,
      mostBookedDay: topDay[0] || null,
      dailyStats
    });
  } catch (err) {
    console.error('Error:', err);
    res.status(500).send('Failed to generate booking summary');
  } finally {
    if (connection) await connection.end();
  }
};
