# "Relay" Implementation

Calling this part Relay, because it's essentially relaying the info between the website, the arduino, and the Supabase backend instance.

### Implementation

Use of different, isolated services for the following:

1. Arduino
2. Database management
3. Socket management

Each service has a class, and those classes are used in a singleton instance called App. Using the App instance, everything can be managed easily.
