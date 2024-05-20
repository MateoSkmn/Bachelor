import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { HeaderComponent } from '../../global/components/header/header.component';
import { StyledButtonComponent } from '../../global/components/styled-button/styled-button.component';
import { Subscription } from 'rxjs';
import { ApiService } from '../../global/service/api.service';
import { ErrorService } from '../../global/service/error.service';
import { ModelListItem } from '../../global/interfaces/model-list-item.interface';
import { ModelTableRowComponent } from './model-table-row/model-table-row.component';
import { RecordListItem } from '../../global/interfaces/record-list-item.interface';

@Component({
  selector: 'app-model',
  standalone: true,
  imports: [HeaderComponent, StyledButtonComponent, ModelTableRowComponent],
  templateUrl: './model.component.html',
  styleUrl: './model.component.scss'
})
export class ModelComponent implements OnInit, OnDestroy {

  @ViewChild('fileInput') fileInput!: ElementRef;

  private modelListSubscription!: Subscription;
  private recordListSubscription!: Subscription;
  private uploadSubscription!: Subscription;

  modelList: ModelListItem[] = [];
  recordList: RecordListItem[] = [];

  constructor(private apiService: ApiService, private errorService: ErrorService) {}

  //Requests data from the BE when the component is loaded
  ngOnInit(): void {
    this.modelListSubscription = this.apiService.getModels().subscribe({
      next: (response) => {
        this.modelList = response;
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });

    this.recordListSubscription = this.apiService.getRecords().subscribe({
      next: (response) => {
        this.recordList = response.filter(item => !item.hasModel);
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });
  }

  //Avoid potential memory leaks by unsubscribing when the component is no longer used
  ngOnDestroy(): void {
    if (this.modelListSubscription) {
      this.modelListSubscription.unsubscribe();
    }
    if (this.uploadSubscription) {
      this.uploadSubscription.unsubscribe();
    }
  }

  /**
   * Button event to open file uploader
   */
  uploadFile(): void {
    this.fileInput.nativeElement.click();
  }

  /**
   * Sends the uplaoded file to the BE
   * @param event Data uploaded by file uploader
   */
  handleFileInput(event: any): void {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    this.uploadSubscription = this.apiService.postModel(formData).subscribe({
      next: (response) => {
        window.location.reload();
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });
  }
}
