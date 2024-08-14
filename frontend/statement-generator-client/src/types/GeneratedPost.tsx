export interface GeneratedPost {
    id: string;
    title: string;
    text: string;
    prompt: string;
    publicOfficialName: {eng: string, heb: string};
    language: string;
    socialMedia: string;
    createdAt: Date;
}