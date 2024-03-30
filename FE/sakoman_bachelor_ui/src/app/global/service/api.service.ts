import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';
import { RecordListItem } from '../interfaces/record-list-item.interface';
import { ModelListItem } from '../interfaces/model-list-item.interface';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private BASE_URL: string = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  // TODO: Weitere & Refactoring

  getRecords(): Observable<RecordListItem[]> {
    const url = `${this.BASE_URL}/data/record`;
    return this.http.get<RecordListItem[]>(url).pipe(
      catchError((error) => {
        return throwError(() => 'FEHLER: Daten konnten nicht geladen werden!');
      })
    );
  }

  getModels(): Observable<ModelListItem[]> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.get<ModelListItem[]>(url).pipe(
      catchError((error) => {
        return throwError(() => 'FEHLER: Daten konnten nicht geladen werden!');
      })
    );
  }

  postRecord(body: FormData): Observable<any> {
    const url = `${this.BASE_URL}/data/record`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => 'FEHLER: Datei konnte nicht hochgeladen werden!');
      })
    );
  }

  postModel(body: FormData): Observable<any> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => 'FEHLER: Datei konnte nicht hochgeladen werden!');
      })
    );
  }

  deleteRecord(file_name: string): Observable<any> {
    const url = `${this.BASE_URL}/data/record/${file_name}`;
    return this.http.delete<any>(url).pipe(
      catchError((error) => {
        return throwError(() => 'FEHLER: Datei konnte nicht gelöscht werden!');
      })
    )
  }

  deleteModel(): Observable<any> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.delete<any>(url).pipe(
      catchError((error) => {
        return throwError(() => 'FEHLER: Datei konnte nicht gelöscht werden!');
      })
    )
  }
}
