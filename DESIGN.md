# Questions Answers

### Why did you choose your specific method for handling the "Ripple Effects"?

I divided my code into three helper functions, each responsible for handling a specific condition in the ripple effect. Then, I created one main helper function that executes the entire ripple effect logic. In the API endpoint, I only call this main helper function. This approach makes the code easier to debug, allows for quick bug fixes, and simplifies the addition of new conditions in the future. It also makes the logic reusable across multiple endpoints, improving maintainability and scalability.

### How would your implementation handle 1,000 status updates per second?

To handle high throughput, I added indexes on machine.id in all relevant tables to speed up joins, and composite indexes on (machine_id, is_open) in the MaintenanceTicket table to quickly identify open tickets for a specific machine. Additionally, I implemented conditional checks within the ripple effect logic to avoid unnecessary updates or inserts in the database. These optimizations reduce the number of queries and updates executed per request, ensuring the system remains performant even under high load.