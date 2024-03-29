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
        console.error('Error fetching data:', error);
        return throwError(() => 'Something went wrong, please try again later.');
      })
    );
  }

  getModels(): Observable<ModelListItem[]> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.get<ModelListItem[]>(url).pipe(
      catchError((error) => {
        console.error('Error fetching data:', error);
        return throwError(() => 'Something went wrong, please try again later.');
      })
    );
  }

  postRecord(body: FormData): Observable<any> {
    const url = `${this.BASE_URL}/data/record`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        console.error('Error uplaoding file:', error);
        return throwError(() => 'Something went wrong, please try again later.');
      })
    );
  }

  postModel(body: FormData): Observable<any> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        console.error('Error uploading file:', error);
        return throwError(() => 'Something went wrong, please try again later.');
      })
    );
  }
}
