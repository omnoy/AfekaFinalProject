export function getDateFromObjectId(objectId: string): Date {
  // Extract the timestamp (in seconds) from the ObjectId
  const timestamp = parseInt(objectId.substring(0, 8), 16);

  // Create a new Date object using the timestamp (converting seconds to milliseconds)
  return new Date(timestamp * 1000);
}