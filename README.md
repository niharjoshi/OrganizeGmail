# OG: Organize Gmail!
Each Google Account includes 15 GB of storage, which is shared across Gmail, Google Drive, and Google Photos. That is NOT enough!

Meet OG, a new way to free up your Gmail inbox and make more space available for the conversations that really matter. List and filter your emails by sender or domain and use the treemap to nuke whatever you don't need. Get rid of those pesky Amazon delivery emails and Zuckerberg's Metaverse spam, with one click of a button.

## Features
- Import all your Google account emails in one place
- Index emails for quick retreival and query support
- Visualize emails by multiple filters across a clustered treemap
- Easily find out who's spamming you or which emails eat up your space
- Delete unwanted emails by sender to free up space instantly
- Built on top of Google's SSO for security

OG isn't just a CRUD app for email management - it's a colourful dashboard that saves you time and enhances your productivity by showcasing an interactive, birdseye view of your Google inbox and identifying the spam for you.

## SSO
OG uses your Google account for authentication so your login is securely handled by the google-auth OAuth servers. We do not handle your usernames or password in our backend in any way.

## Tech Stack

## MVP
(Placeholder Vercel URL for our app: [Organize Gmail](http://organize-gmail.vercel.app/))

Our goal for the minimum viable product is to deliver a Django dashboard hosted on Vercel that logs you in with Google's SSO and helps you visualize your Gmail inbox by filters like sender and domain.

However, our final aim is to allow the user to mass delete emails based on the selected filter. We will also try to include the recompression of attachments feature to save even more Google Drive space.
