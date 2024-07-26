export interface PublicOfficial {
    id: string,
    full_name: {eng: string, heb: string},
    position: {eng: string, heb: string},
    age: number | null,
    political_party: {eng: string, heb: string} | null,
    social_media_handles: {social_media: string, handle: string}[]
}