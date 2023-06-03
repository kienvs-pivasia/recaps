import unauthorizedRequest from "@/config/unauthorizedRequest";

interface NewCaptionBody {
  content: string;
  idUser: number;
  trangThai: boolean;
  tags?: string[];
  favourite?: boolean;
  userId?: string;
}

interface NewCaptionBody {
  Content: string;
  IDCaption: number;
  TrangThai: boolean;
  IDTag: string;
  IDUser: string;
}
export function getListCaptions() {
  return unauthorizedRequest.get(`/function/getListCaption`);
}

export function addNewCaption(body: NewCaptionBody) {
  return unauthorizedRequest.post(`/AddCaption/new`, body);
}

export function updateCaption(params: any) {
  return unauthorizedRequest.put(`/UpdateCaption`, params);
}

export function deleteCaption(params: string) {
  return unauthorizedRequest.delete(`/removeCaption?idCaption=${params}`);
}
