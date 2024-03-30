import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { HeaderComponent } from '../../global/components/header/header.component';
import { StyledButtonComponent } from '../../global/components/styled-button/styled-button.component';
import { ApiService } from '../../global/service/api.service';
import { Subscription } from 'rxjs';
import { RecordListItem } from '../../global/interfaces/record-list-item.interface';
import { RecordTableRowComponent } from './record-table-row/record-table-row.component';
import { ErrorService } from '../../global/service/error.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [HeaderComponent, StyledButtonComponent, RecordTableRowComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit, OnDestroy {

  @ViewChild('fileInput') fileInput!: ElementRef;

  private recordListSubscription!: Subscription;
  private uploadSubscription!: Subscription;

  recordList: RecordListItem[] = [];

  constructor(private apiService: ApiService, private errorService: ErrorService) {}

  ngOnInit(): void {
    this.recordListSubscription = this.apiService.getRecords().subscribe({
      next: (response) => {
        this.recordList = response;
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });
  }

  ngOnDestroy(): void {
    if (this.recordListSubscription) {
      this.recordListSubscription.unsubscribe();
    }
    if (this.uploadSubscription) {
      this.uploadSubscription.unsubscribe();
    }
  }

  uploadFile(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: any): void {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    this.uploadSubscription = this.apiService.postRecord(formData).subscribe({
      next: (response) => {
        console.log(response);
        window.location.reload();
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });
  }
}
